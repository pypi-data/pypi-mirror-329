class Mail:
    @staticmethod
    def SendMail(user: str = '', pwd: str = '', sender: str = '', title: str = '', content: str = '', to: str | list = '', cc: str | list = None, attr: str | list = None, server: str = 'smtp.qq.com', port: int = 465, ssl: bool = True, timeout: int = 10, continueOnError: bool = False):
        '''
        发送邮件

        Mail.SendMail(user=\'\', pwd=\'\', sender=\'\', title=\'\', content=\'\', to=\'\', cc=None, attr=None, server="smtp.qq.com", port=465, ssl=True, timeout=10, continueOnError=False)

        :param user: [必选参数]邮箱登录帐号，比如普通QQ邮箱的登录帐号与邮箱地址相同
        :param pwd: [必选参数]登录密码
        :param sender: [必选参数]发件人邮箱地址
        :param title: [必选参数]邮件的标题
        :param content: [必选参数]邮件正文内容，支持HTML类型的正文内容
        :param to: [必选参数]收件人邮箱地址，多个地址可用["xxx@qq.com","xxx@163.com"]列表的形式填写, 也可以是单个邮箱地址字符串
        :param cc: [可选参数]抄送邮箱地址，多个地址可用["xxx@qq.com","xxx@163.com"]列表的形式填写, 也可以是单个邮箱地址字符串, None:不需要抄送，默认None
        :param attr: [可选参数]邮件附件，多个附件可以用["附件一路径","附件二路径"]列表的形式填写，也可以是单个附件路径字符串, None:不需要附件，默认None
        :param server: [可选参数]SMTP服务器地址，默认smtp.qq.com
        :param port: [可选参数]SMTP服务器端口，常见为 25、465、587，默认465
        :param ssl: [可选参数]是否使用SSL协议加密，True为使用，False为不使用，默认True
        :param timeout: [可选参数]超时时间(秒)，默认10
        :param continueOnError: [可选参数]发生错误是否继续，True为继续，False为不继续。默认False
        :return:None
        '''
