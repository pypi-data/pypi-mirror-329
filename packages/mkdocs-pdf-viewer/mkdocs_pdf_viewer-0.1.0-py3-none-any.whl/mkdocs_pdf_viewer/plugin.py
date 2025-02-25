import re, uuid
from mkdocs.plugins import BasePlugin

class PDFViewerPlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, files):
        return self.convert_pdf_viewers(markdown)

    def convert_pdf_viewers(self, text):
        # Regex matches ![Alt text](<pdf-url>){ type=application/pdf viewer }
        pattern = re.compile(r'!\[(.*?)\]\(<([^>]+)>\)\{[^}]*type=application/pdf[^}]*viewer[^}]*\}')

        def repl(m):
            alt = m.group(1).strip() or "View PDF"
            url = m.group(2).strip()
            mid = "pdf-modal-" + str(uuid.uuid4())
            # All HTML is in one line to avoid extra spaces/newlines
            # Using a <span> wrapper with inline display
            return (
                f'<span style="display:inline;">'
                f'<a href="#" class="pdf-modal-link" data-modal-id="{mid}" data-pdf-url="{url}">{alt}</a>'
                f'<div id="{mid}" class="pdf-modal"><div class="pdf-modal-content">'
                f'<span class="pdf-modal-close">&times;</span>'
                f'<iframe src="{url}" frameborder="0"></iframe>'
                f'</div></div>'
                f'</span>'
            )

        return pattern.sub(repl, text)

    def on_post_page(self, output, page, config):
        if 'pdf-modal-link' in output:
            output += self._style() + self._script()
        return output

    def _script(self):
        return (
            '<script>'
            'document.addEventListener("DOMContentLoaded",function(){'
            'function openModal(m){m.style.display="block";m.querySelector(".pdf-modal-content").classList.add("zoom-out");}'
            'function closeModal(m){m.querySelector(".pdf-modal-content").classList.remove("zoom-out");m.style.display="none";}'
            'document.querySelectorAll(".pdf-modal-link").forEach(function(link){'
            'var m=document.getElementById(link.getAttribute("data-modal-id"));'
            'var c=m.querySelector(".pdf-modal-close");'
            'link.addEventListener("click",function(e){e.preventDefault();openModal(m);});'
            'c.addEventListener("click",function(){closeModal(m);});'
            'window.addEventListener("click",function(e){if(e.target==m){closeModal(m);}});'
            '});'
            '});'
            '</script>'
        )

    def _style(self):
        return (
            '<style>'
            '.pdf-modal {'
            '  display:none;position:fixed;top:0;left:0;width:100%;height:100%;'
            '  background:rgba(0,0,0,0.8);z-index:1000;overflow:auto;'
            '  padding:2%;box-sizing:border-box;'
            '}'
            '.pdf-modal-content {'
            '  position:relative;width:100%;height:100%;background:#fff;'
            '  border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,0.5);overflow:hidden;'
            '  transform:scale(0.8);transition:transform 0.3s ease;'
            '}'
            '.pdf-modal-content.zoom-out {transform:scale(1);}'
            '.pdf-modal-close {'
            '  position:absolute;top:10px;right:10px;font-size:30px;font-weight:bold;'
            '  color:#333;background:#fff;border-radius:50%;width:40px;height:40px;'
            '  line-height:40px;text-align:center;cursor:pointer;z-index:1100;'
            '}'
            '.pdf-modal-close:hover {color:#000;}'
            '.pdf-modal-content iframe {width:100%;height:100%;border:none;}'
            '.pdf-modal-link {'
            '  text-decoration:none;color:#007bff;'
            '  margin:0 4px;transition:color 0.3s ease,transform 0.3s ease;'
            '}'
            '.pdf-modal-link:hover {color:#0056b3;transform:scale(1.05);}'
            '</style>'
        )
