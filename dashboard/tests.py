from django.test import TestCase


class PublicPageTests(TestCase):
    def test_index_ok(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "台灣車輛資訊分析網")
        self.assertNotContains(response, "C111")
        self.assertNotContains(response, "C110")
        self.assertContains(response, "Lrniey666")

    def test_ranking_empty_ok(self):
        response = self.client.get("/rankings/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "尚無資料")

    def test_admin_not_in_nav(self):
        response = self.client.get("/")
        self.assertNotContains(response, 'href="/admin/"')
