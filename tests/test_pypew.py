import unittest
from unittest.mock import patch

from flask import url_for

from pypew import create_app


class TestViews(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.app.config['SERVER_NAME'] = 'localhost:5000'
        self.app.app_context().push()
        self.client = self.app.test_client()

    def test_index_view(self):
        r = self.client.get(url_for('index_view'))
        self.assertEqual(r.status_code, 200)

    def test_service_index_view(self):
        r = self.client.get(url_for('service_index_view'))
        self.assertEqual(r.status_code, 200)

    def test_service_detail_view(self):
        r = self.client.get(
            url_for('service_detail_view', name='Christmas Day')
        )
        self.assertEqual(r.status_code, 200)

    def test_service_detail_view_handles_not_found(self):
        r = self.client.get(
            url_for('service_detail_view', name='Notmas Day')
        )
        self.assertEqual(r.status_code, 404)

    @patch('pypew.views.Service.create_docx')
    def test_service_docx_view(self, m_create_docx):
        r = self.client.get(
            url_for('service_docx_view', name='Christmas Day')
        )
        m_create_docx.assert_called()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Disposition'],
            'attachment; filename="Christmas Day.docx"')
        self.assertEqual(
            r.headers['Content-Type'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    @unittest.expectedFailure
    @patch('pypew.views.convert')
    @patch('pypew.views.Service.create_docx')
    def test_service_pdf_view(self, m_create_docx, m_convert):
        r = self.client.get(
            url_for('service_pdf_view', name='Christmas Day')
        )
        m_convert.assert_called()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Disposition'],
                         'attachment; filename="Christmas Day.pdf"')


if __name__ == '__main__':
    unittest.main()
