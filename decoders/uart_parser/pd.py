import sigrokdecode as srd

class Decoder(srd.Decoder):
    api_version = 3
    id          = 'uart_parser'
    name        = '串口解析'
    longname    = '串口解析'
    desc        = '简易的串口解析'
    license     = 'gplv2+'
    inputs      = ['logic']
    outputs     = [] 
    tags        = ['我的解析']

    options     = (
        {'id': 'baudrate', 'desc': '波特率', 'default': 115200},
    )
    channels = (
        {'id': 'data', 'name': '数据线', 'desc': '数据线'},
    )

    annotations = (
        ('bit',   '比特'),
        ('byte',  '字节'),
        ('start', '起始位'),
        ('stop',  '停止位'),
    )

    annotation_rows = (
        ('bits',  '比特', (0,)),
        ('bytes', '字节', (1,2,3,)),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.samplerate = None
        self.bit_width = 0
        self.bit_count = 0
        self.byte_value = 0
        self.start_sample = 0

    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.samplerate = value
            self.bit_width = float(self.samplerate) / float(self.options['baudrate'])

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def decode(self):
        if not self.samplerate:
            raise Exception("未设置采样率")

        while True:
            # 等待起始位(下降沿)
            self.wait({0: 'f'}) 
            self.start_sample = self.samplenum
            
            # 等待起始位中间点
            self.wait({'skip': int(self.bit_width/2)})
            
            # 显示起始位
            self.put(self.start_sample, self.start_sample + int(self.bit_width), self.out_ann, [2, ['Start', 'S']])

            # 读取8位数据
            self.byte_value = 0
            for i in range(8):

                # 等待下一位
                self.wait({'skip': int(self.bit_width)})
                (data,) = self.wait()  

                # 显示每一位的值
                bit_start = self.start_sample + int(self.bit_width * (i + 1))
                self.put(bit_start, bit_start + int(self.bit_width), self.out_ann, [0, [str(data)]])
                
                self.byte_value |= (data << i)

            # 等待停止位中间点
            self.wait({'skip': int(self.bit_width)})
            
            # 显示停止位
            stop_start = self.start_sample + int(self.bit_width * 9)
            self.put(stop_start, stop_start + int(self.bit_width), self.out_ann, [3, ['Stop', 'P']])

            # 显示完整字节值
            self.put(self.start_sample + int(self.bit_width), stop_start, self.out_ann, [1, ['%02x' % self.byte_value]])

