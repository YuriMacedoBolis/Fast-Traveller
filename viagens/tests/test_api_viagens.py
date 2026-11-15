from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from viagens.models import AtracaoViagem, Categoria, Viagem

Usuario = get_user_model()


class ApiViagensTest(TestCase):
    def setUp(self):
        self.ana = Usuario.objects.create_user(
            username="ana", email="ana@exemplo.com", password="senha-forte-123"
        )
        self.bruno = Usuario.objects.create_user(
            username="bruno", email="bruno@exemplo.com", password="senha-forte-123"
        )
        self.museu = Categoria.objects.create(
            nome="Museu", slug="museu", custo_medio=Decimal("50.00")
        )
        self.cinema = Categoria.objects.create(
            nome="Cinema", slug="cinema", custo_medio=Decimal("24.00")
        )
        self.viagem = Viagem.objects.create(
            usuario=self.ana,
            destino="São Paulo, SP",
            duracao_dias=3,
            orcamento_total=Decimal("1500.00"),
            data_inicio=date.today() + timedelta(days=10),
        )

    def test_listar_exige_autenticacao(self):
        resposta = self.client.get("/api/v1/viagens/")
        self.assertIn(resposta.status_code, (401, 403))

    def test_criar_viagem(self):
        self.client.force_login(self.ana)
        resposta = self.client.post(
            "/api/v1/viagens/",
            {
                "destino": "Rio de Janeiro, RJ",
                "duracao_dias": 2,
                "orcamento_total": "800.00",
                "data_inicio": str(date.today() + timedelta(days=20)),
            },
            content_type="application/json",
        )
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.json()["destino"], "Rio de Janeiro, RJ")
        self.assertEqual(Viagem.objects.get(pk=resposta.json()["id"]).usuario, self.ana)

    def test_criar_viagem_com_orcamento_invalido(self):
        self.client.force_login(self.ana)
        resposta = self.client.post(
            "/api/v1/viagens/",
            {
                "destino": "Curitiba, PR",
                "duracao_dias": 2,
                "orcamento_total": "-10.00",
                "data_inicio": str(date.today() + timedelta(days=5)),
            },
            content_type="application/json",
        )
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("orcamento_total", resposta.json())

    def test_criar_viagem_com_data_passada(self):
        self.client.force_login(self.ana)
        resposta = self.client.post(
            "/api/v1/viagens/",
            {
                "destino": "Salvador, BA",
                "duracao_dias": 2,
                "orcamento_total": "500.00",
                "data_inicio": str(date.today() - timedelta(days=1)),
            },
            content_type="application/json",
        )
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("data_inicio", resposta.json())

    def test_lista_mostra_apenas_viagens_do_usuario(self):
        self.client.force_login(self.bruno)
        resposta = self.client.get("/api/v1/viagens/")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json(), [])

    def test_viagem_de_outro_usuario_retorna_404(self):
        self.client.force_login(self.bruno)
        for rota in ["", "atracoes/", "relatorio/"]:
            resposta = self.client.get(f"/api/v1/viagens/{self.viagem.pk}/{rota}")
            self.assertEqual(resposta.status_code, 404)

    def test_busca_por_destino(self):
        self.client.force_login(self.ana)
        resposta = self.client.get("/api/v1/viagens/?destino=paulo")
        self.assertEqual(len(resposta.json()), 1)
        resposta = self.client.get("/api/v1/viagens/?destino=recife")
        self.assertEqual(len(resposta.json()), 0)

    def test_busca_com_valor_invalido_retorna_400(self):
        self.client.force_login(self.ana)
        resposta = self.client.get("/api/v1/viagens/?orcamento_min=abc")
        self.assertEqual(resposta.status_code, 400)

    def test_relatorio_reproduz_exemplo_do_contrato(self):
        AtracaoViagem.objects.create(
            viagem=self.viagem,
            categoria=self.museu,
            nome="MASP",
            custo_estimado=Decimal("50.00"),
            tempo_estimado_horas=Decimal("2.50"),
        )
        AtracaoViagem.objects.create(
            viagem=self.viagem,
            categoria=self.cinema,
            nome="Cine Sesc",
            custo_estimado=Decimal("24.00"),
            tempo_estimado_horas=Decimal("2.00"),
        )
        self.client.force_login(self.ana)
        dados = self.client.get(f"/api/v1/viagens/{self.viagem.pk}/relatorio/").json()

        self.assertEqual(dados["custo_total_estimado"], "74.00")
        self.assertEqual(dados["saldo_restante"], "1426.00")
        self.assertEqual(dados["total_atracoes"], 2)
        self.assertEqual(
            dados["gastos_por_categoria"], {"museu": "50.00", "cinema": "24.00"}
        )

    def test_relatorio_sem_atracoes(self):
        self.client.force_login(self.ana)
        dados = self.client.get(f"/api/v1/viagens/{self.viagem.pk}/relatorio/").json()
        self.assertEqual(dados["custo_total_estimado"], "0.00")
        self.assertEqual(dados["total_atracoes"], 0)
        self.assertEqual(dados["gastos_por_categoria"], {})

    def test_adicionar_e_remover_atracao(self):
        self.client.force_login(self.ana)
        resposta = self.client.post(
            f"/api/v1/viagens/{self.viagem.pk}/atracoes/",
            {
                "nome": "Pinacoteca",
                "categoria": "museu",
                "custo_estimado": "30.00",
                "tempo_estimado_horas": "2.00",
                "endereco": "Praça da Luz",
                "api_external_id": "abc123",
            },
            content_type="application/json",
        )
        self.assertEqual(resposta.status_code, 201)
        atracao_id = resposta.json()["id"]

        resposta = self.client.delete(
            f"/api/v1/viagens/{self.viagem.pk}/atracoes/{atracao_id}/"
        )
        self.assertEqual(resposta.status_code, 204)
        self.assertEqual(self.viagem.atracoes.count(), 0)

    def test_atualizar_e_excluir_viagem(self):
        self.client.force_login(self.ana)
        resposta = self.client.put(
            f"/api/v1/viagens/{self.viagem.pk}/",
            {
                "destino": "São Paulo, SP",
                "duracao_dias": 4,
                "orcamento_total": "1800.00",
                "data_inicio": str(date.today() + timedelta(days=10)),
            },
            content_type="application/json",
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["duracao_dias"], 4)

        resposta = self.client.delete(f"/api/v1/viagens/{self.viagem.pk}/")
        self.assertEqual(resposta.status_code, 204)
        self.assertEqual(Viagem.objects.count(), 0)
