from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QTextDocument,QTextCursor
from PyQt5.QtCore import Qt

def htmll(name, gender, age, custom_info):
    html_content = f'''
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            font-size: 14px;
                        }}
                        b {{
                            color: #336699;
                        }}
                        .info {{
                            margin-left: 20px;
                        }}
                    </style>
                </head>
                <body>
                    <h1>实验报告</h1>
                    <div class="info">
                        <b>姓名:</b> {name}<br>
                        <b>性别:</b> {gender}<br>
                        <b>年龄:</b> {age}<br>
                        <b>检测报告:</b> {custom_info}
                    </div>
                </body>
                </html>
            '''

    # 创建 QTextDocument 并设置 HTML 内容
    text_document = QTextDocument()
    text_document.setHtml(html_content)

    # 使用 QTextCursor 将 HTML 内容插入到文档中
    cursor = QTextCursor(text_document)
    cursor.movePosition(QTextCursor.Start)

    # 打开一个文件以写入HTML内容
    namee=name+'.html'
    with open(namee, 'w') as file:
        # 将HTML内容写入文件
        file.write(text_document.toHtml())

if __name__ == '__main__':
    # 调用函数创建HTML文件
    htmll("张三", "男", 25, 3, "目前来看，未在测试者身上检测出注意缺陷多动障碍，被测试者全程注意力集中。")
