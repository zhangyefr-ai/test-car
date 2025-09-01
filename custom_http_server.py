import http.server
import socketserver

PORT = 8000  # 你可以更改端口号

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        # 先调用父类方法获取默认的 MIME 类型猜测
        base_type = super().guess_type(path)
        # 检查文件路径是否以 .br 结尾
        if path.endswith(".br"):
            # 对于 .br 文件，返回 Brotli 压缩数据的 MIME 类型
            return "application/x-brotli"
        # 如果不是 .br 文件，返回父类猜测的类型
        return base_type

    def end_headers(self):
        # 可选：如果你希望服务器声明内容编码，并且确定文件是预压缩的 .br 文件
        # 注意：这需要谨慎使用，通常 .br 文件作为静态资源直接服务时，
        # 可能需要根据对应的原始文件设置 Content-Type 和 Content-Encoding
        # 例如，对于 example.txt.br，应设置：
        # Content-Type: text/plain
        # Content-Encoding: br
        # 下面的代码是一个更高级处理的简化示例，可能需要根据你的具体需求调整
        if self.path.endswith('.br'):
            # 尝试从路径中推断原始文件的 MIME 类型
            original_path = self.path.rsplit('.br', 1)[0]
            original_mime = super().guess_type(original_path)
            if original_mime:
                self.send_header('Content-Type', original_mime)
            self.send_header('Content-Encoding', 'br')
        # 必须调用父类的 end_headers 来发送头部
        super().end_headers()

# 设置服务器监听的地址和端口
with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()