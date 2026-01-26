import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_package.executors import *
from selenium_package.interfaces import *
from selenium_package.actions import *

from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.utils.utils import html_to_base64_pdf
from automacao_certificados.selenium_automations.adapters.extractors import CertificadoDelmiroExtractor
from ..locators import locators
class DownloadPage(DownloadPagePort):
    def __init__(
        self, 
        driver: WebDriver,
    ):
        self.driver = driver

    def go_to_download_page_executor(
        self,
    ) -> BaseExecutor:
        """
        Go to the download page.
        To execute an executor the method 'run()' must be called.
        """
        desired_tab_title = "agilicloud"
        desired_url = "EmitirRelatorio"

        action = GoToTabThatContainsTitle(
            self.driver,
            desired_tab_title=desired_tab_title
        )
        executor = RetryActionUntilUrlContains(
            action=action,
            desired_url=desired_url
        )

        return executor

    def get_certificado_base64_pdf_executor(
        self,
    ) -> BaseExecutor:
        """
        Get the certificado base64 pdf.
        Extracts the complete HTML with styles from the page and generates a single-page PDF.
        To execute an executor the method 'run()' must be called.
        """
        # Get the report panel element (contains the actual certificate content)
        report_panel = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(locators.CERTIFICADO_IMAGE_LOCATOR)
        )

        # Extract the complete HTML with styles from the page
        extract_html_script = """
        // Get all style tags from the document
        var styleTags = document.querySelectorAll('style');
        var stylesContent = '';
        for (var i = 0; i < styleTags.length; i++) {
            stylesContent += styleTags[i].outerHTML + '\\n';
        }

        // Get the report panel HTML (the actual certificate content)
        var reportPanel = arguments[0];
        var reportContent = reportPanel.innerHTML;

        return {
            styles: stylesContent,
            content: reportContent
        };
        """

        # Execute script to extract styles and content
        result = self.driver.execute_script(extract_html_script, report_panel)
        styles_html = result['styles']
        report_content_html = result['content']

        # Calculate content dimensions and determine if scaling is needed
        calculate_dimensions_script = """
        var reportPanel = arguments[0];
        var rect = reportPanel.getBoundingClientRect();
        var height = rect.height || reportPanel.scrollHeight || reportPanel.offsetHeight;
        var width = rect.width || reportPanel.scrollWidth || reportPanel.offsetWidth;

        // A4 dimensions in pixels (at 96 DPI): 794px x 1123px
        // We'll use a safe height of ~1100px to account for margins
        var maxHeight = 1100;
        var maxWidth = 794;

        var scaleX = 1;
        var scaleY = 1;

        if (width > maxWidth) {
            scaleX = maxWidth / width;
        }
        if (height > maxHeight) {
            scaleY = maxHeight / height;
        }

        // Use the smaller scale to ensure everything fits
        var scale = Math.min(scaleX, scaleY, 1);

        return {
            height: height,
            width: width,
            scale: scale
        };
        """

        dimensions = self.driver.execute_script(calculate_dimensions_script, report_panel)
        content_scale = dimensions['scale']

        # Create complete HTML document with original styles and report content
        # Using aggressive CSS to force single page output
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    {styles_html}
    <style>
        @page {{
            margin: 0;
            size: A4;
            overflow: hidden;
        }}
        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }}
        body {{
            display: flex;
            align-items: flex-start;
            justify-content: flex-start;
        }}
        /* Container to hold and scale content */
        #certificate-container {{
            width: 100%;
            transform-origin: top left;
            transform: scale({content_scale});
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }}
        /* Prevent ALL page breaks - very aggressive */
        * {{
            page-break-inside: avoid !important;
            break-inside: avoid !important;
            page-break-after: avoid !important;
            break-after: avoid !important;
            page-break-before: avoid !important;
            break-before: avoid !important;
        }}
        /* Ensure table doesn't break across pages */
        table {{
            page-break-inside: avoid !important;
            break-inside: avoid !important;
            width: 100%;
            border-collapse: collapse;
        }}
        tr {{
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }}
        td, th {{
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }}
        /* Prevent any element from causing page breaks */
        div, p, span, h1, h2, h3, h4, h5, h6 {{
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }}
    </style>
</head>
<body>
    <div id="certificate-container">
        {report_content_html}
    </div>
</body>
</html>"""

        return html_to_base64_pdf(html=html)


    def run(
        self,
    ) -> None:
        """
        Run the download page.
        To execute an executor the method 'run()' must be called.
        """
        self.go_to_download_page_executor().run()
        pdf = self.get_certificado_base64_pdf_executor()
        document_extracted = CertificadoDelmiroExtractor(driver=self.driver).run()
        return document_extracted, pdf