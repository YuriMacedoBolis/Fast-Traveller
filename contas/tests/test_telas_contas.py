from django.contrib.auth import get_user_model
from django.test import TestCase

Usuario = get_user_model()


class TelasContasTest(TestCase):
    def setUp(self):
        self.ana = Usuario.objects.create_user(
            username="ana", email="ana@exemplo.com", password="senha-forte-123"
        )

    def test_cadastro_cria_usuario_e_faz_login(self):
        resposta = self.client.post(
            "/cadastro/",
            {
                "first_name": "Carla",
                "username": "carla",
                "email": "Carla@Exemplo.com",
                "password1": "viagem-segura-987",
                "password2": "viagem-segura-987",
            },
        )
        self.assertRedirects(resposta, "/viagens/")
        carla = Usuario.objects.get(username="carla")
        self.assertEqual(carla.email, "carla@exemplo.com")
        self.assertEqual(int(self.client.session["_auth_user_id"]), carla.pk)

    def test_cadastro_com_email_repetido(self):
        resposta = self.client.post(
            "/cadastro/",
            {
                "first_name": "Outra Ana",
                "username": "ana2",
                "email": "ANA@exemplo.com",
                "password1": "viagem-segura-987",
                "password2": "viagem-segura-987",
            },
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("email", resposta.context["form"].errors)
        self.assertFalse(Usuario.objects.filter(username="ana2").exists())

    def test_login_com_dados_corretos(self):
        resposta = self.client.post(
            "/login/", {"username": "ana", "password": "senha-forte-123"}
        )
        self.assertRedirects(resposta, "/viagens/")

    def test_login_com_senha_errada(self):
        resposta = self.client.post("/login/", {"username": "ana", "password": "errada"})
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Usuário ou senha incorretos.")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_encerra_a_sessao(self):
        self.client.force_login(self.ana)
        resposta = self.client.post("/logout/")
        self.assertRedirects(resposta, "/")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_usuario_logado_nao_ve_cadastro(self):
        self.client.force_login(self.ana)
        resposta = self.client.get("/cadastro/")
        self.assertRedirects(resposta, "/viagens/")
