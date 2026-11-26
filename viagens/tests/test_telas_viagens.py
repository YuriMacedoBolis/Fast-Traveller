from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from viagens.models import AtracaoViagem, Categoria, Viagem
from viagens.views import texto_seguro

Usuario = get_user_model()


class BaseTelasTest(TestCase):
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
            orcamento_total=Decimal("100.00"),
            data_inicio=date.today() + timedelta(days=10),
        )

    def adicionar_atracao(self, nome, categoria, custo):
        return AtracaoViagem.objects.create(
            viagem=self.viagem,
            categoria=categoria,
            nome=nome,
            custo_estimado=Decimal(custo),
            tempo_estimado_horas=Decimal("2.00"),
        )


class ListaViagensTest(BaseTelasTest):
    def test_lista_exige_login(self):
        resposta = self.client.get("/viagens/")
        self.assertRedirects(resposta, "/login/?next=/viagens/")

    def test_lista_mostra_apenas_viagens_do_usuario(self):
        self.client.force_login(self.bruno)
        resposta = self.client.get("/viagens/")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.context["viagens"]), 0)

    def test_busca_por_destino(self):
        self.client.force_login(self.ana)
        resposta = self.client.get("/viagens/?destino=paulo")
        self.assertEqual(len(resposta.context["viagens"]), 1)
        resposta = self.client.get("/viagens/?destino=recife")
        self.assertEqual(len(resposta.context["viagens"]), 0)

    def test_cartao_tem_link_para_o_roteiro(self):
        self.client.force_login(self.ana)
        resposta = self.client.get("/viagens/")
        self.assertContains(resposta, f'href="/viagens/{self.viagem.pk}/"')


class CrudViagemTest(BaseTelasTest):
    def test_criar_viagem_leva_para_o_roteiro(self):
        self.client.force_login(self.ana)
        resposta = self.client.post(
            "/viagens/nova/",
            {
                "destino": "Recife, PE",
                "data_inicio": str(date.today() + timedelta(days=5)),
                "duracao_dias": 2,
                "orcamento_total": "900.00",
            },
        )
        nova = Viagem.objects.get(destino="Recife, PE")
        self.assertEqual(nova.usuario, self.ana)
        self.assertRedirects(resposta, f"/viagens/{nova.pk}/")

    def test_criar_viagem_com_data_passada(self):
        self.client.force_login(self.ana)
        resposta = self.client.post(
            "/viagens/nova/",
            {
                "destino": "Recife, PE",
                "data_inicio": str(date.today() - timedelta(days=1)),
                "duracao_dias": 2,
                "orcamento_total": "900.00",
            },
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("data_inicio", resposta.context["form"].errors)
        self.assertFalse(Viagem.objects.filter(destino="Recife, PE").exists())

    def test_editar_viagem(self):
        self.client.force_login(self.ana)
        resposta = self.client.post(
            f"/viagens/{self.viagem.pk}/editar/",
            {
                "destino": "Campinas, SP",
                "data_inicio": str(self.viagem.data_inicio),
                "duracao_dias": 4,
                "orcamento_total": "250.00",
            },
        )
        self.assertRedirects(resposta, "/viagens/")
        self.viagem.refresh_from_db()
        self.assertEqual(self.viagem.destino, "Campinas, SP")
        self.assertEqual(self.viagem.orcamento_total, Decimal("250.00"))

    def test_nao_edita_nem_exclui_viagem_de_outro_usuario(self):
        self.client.force_login(self.bruno)
        self.assertEqual(self.client.get(f"/viagens/{self.viagem.pk}/editar/").status_code, 404)
        self.assertEqual(self.client.post(f"/viagens/{self.viagem.pk}/excluir/").status_code, 404)
        self.assertTrue(Viagem.objects.filter(pk=self.viagem.pk).exists())

    def test_excluir_viagem(self):
        self.client.force_login(self.ana)
        resposta = self.client.post(f"/viagens/{self.viagem.pk}/excluir/")
        self.assertRedirects(resposta, "/viagens/")
        self.assertFalse(Viagem.objects.filter(pk=self.viagem.pk).exists())


class RoteiroTest(BaseTelasTest):
    def test_roteiro_exige_login(self):
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/")
        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login/", resposta.url)

    def test_roteiro_de_outro_usuario_retorna_404(self):
        self.client.force_login(self.bruno)
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/")
        self.assertEqual(resposta.status_code, 404)

    def test_roteiro_mostra_categorias_e_atracoes_salvas(self):
        self.adicionar_atracao("MASP", self.museu, "50.00")
        self.client.force_login(self.ana)
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/")

        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, "viagens/roteiro.html")
        self.assertContains(resposta, 'value="museu"')
        self.assertContains(resposta, 'value="cinema"')
        self.assertEqual(len(resposta.context["atracoes"]), 1)
        self.assertEqual(resposta.context["atracoes"][0]["nome"], "MASP")
        self.assertContains(resposta, 'id="dados-atracoes"')
        self.assertContains(resposta, 'data-orcamento="100.00"')

    def test_roteiro_escapa_nome_da_atracao(self):
        self.adicionar_atracao("<script>alert(1)</script>", self.museu, "10.00")
        self.client.force_login(self.ana)
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/")
        self.assertNotContains(resposta, "<script>alert(1)</script>")


class RelatorioTest(BaseTelasTest):
    def test_relatorio_de_outro_usuario_retorna_404(self):
        self.client.force_login(self.bruno)
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/relatorio/")
        self.assertEqual(resposta.status_code, 404)

    def test_relatorio_calcula_indicadores_e_gastos(self):
        self.adicionar_atracao("MASP", self.museu, "50.00")
        self.adicionar_atracao("Pinacoteca", self.museu, "25.00")
        self.adicionar_atracao("Cine Sesc", self.cinema, "25.00")
        self.client.force_login(self.ana)
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/relatorio/")

        self.assertEqual(resposta.status_code, 200)
        relatorio = resposta.context["relatorio"]
        self.assertEqual(relatorio["custo_total_estimado"], Decimal("100.00"))
        self.assertEqual(relatorio["saldo_restante"], Decimal("0.00"))
        self.assertEqual(resposta.context["uso_orcamento"], Decimal("100"))

        gastos = resposta.context["gastos"]
        self.assertEqual(gastos[0]["nome"], "Museu")
        self.assertEqual(gastos[0]["valor"], Decimal("75.00"))
        self.assertEqual(gastos[0]["porcentagem"], Decimal("75"))
        self.assertContains(resposta, 'data-porcentagem="75"')

    def test_relatorio_avisa_quando_passa_do_orcamento(self):
        self.adicionar_atracao("MASP", self.museu, "130.00")
        self.client.force_login(self.ana)
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/relatorio/")
        self.assertContains(resposta, "O roteiro passou do orçamento em R$ 30,00")

    def test_relatorio_sem_atracoes(self):
        self.client.force_login(self.ana)
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/relatorio/")
        self.assertEqual(resposta.context["gastos"], [])
        self.assertContains(resposta, "Nenhuma atração no roteiro")

    def test_relatorio_tem_botoes_de_imprimir_e_csv(self):
        self.client.force_login(self.ana)
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/relatorio/")
        self.assertContains(resposta, 'id="botao-imprimir"')
        self.assertContains(resposta, f"/viagens/{self.viagem.pk}/relatorio/csv/")


class ExportarCsvTest(BaseTelasTest):
    def test_exporta_csv(self):
        self.adicionar_atracao("MASP", self.museu, "50.00")
        self.client.force_login(self.ana)
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/relatorio/csv/")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn("attachment", resposta["Content-Disposition"])

        conteudo = resposta.content.decode("utf-8-sig")
        self.assertIn("Destino;São Paulo, SP", conteudo)
        self.assertIn("Saldo;50,00", conteudo)
        self.assertIn("Museu;50,00", conteudo)
        self.assertIn("MASP;Museu;;2,00;50,00", conteudo)

    def test_csv_de_outro_usuario_retorna_404(self):
        self.client.force_login(self.bruno)
        resposta = self.client.get(f"/viagens/{self.viagem.pk}/relatorio/csv/")
        self.assertEqual(resposta.status_code, 404)

    def test_csv_neutraliza_formulas(self):
        self.adicionar_atracao("=HYPERLINK(\"http://x\")", self.museu, "10.00")
        self.client.force_login(self.ana)
        conteudo = self.client.get(f"/viagens/{self.viagem.pk}/relatorio/csv/").content.decode("utf-8-sig")
        self.assertIn("'=HYPERLINK", conteudo)

    def test_texto_seguro(self):
        self.assertEqual(texto_seguro("=1+1"), "'=1+1")
        self.assertEqual(texto_seguro("@SOMA"), "'@SOMA")
        self.assertEqual(texto_seguro("MASP"), "MASP")
        self.assertEqual(texto_seguro(""), "")


class CabecalhosSegurancaTest(BaseTelasTest):
    def test_paginas_enviam_csp_e_permissions_policy(self):
        resposta = self.client.get("/login/")
        self.assertIn("default-src 'self'", resposta["Content-Security-Policy"])
        self.assertIn("frame-ancestors 'none'", resposta["Content-Security-Policy"])
        self.assertIn("camera=()", resposta["Permissions-Policy"])
