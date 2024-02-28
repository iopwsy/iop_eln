# -*- encoding: utf-8 -*-
'''
@File    :   iop_eln.py
@Project :   
@Time    :   2023/10/22 20:14:54
@Author  :   Siyuan Wu 
@Version :   1.0
@Contact :   sywu@iphy.ac.cn
'''

import os, requests, datetime
from typing import Dict, List, Union
import pandas as pd

class eln_Module():
    """
    物理所电子实验平台数据模块基本类
    """
    def __init__(self,
                 module_name:str,
                 module_type:str,
                 module_data:Union[
                                   Dict[str,str], ### 表单模块-文本项/多行文本项/日期相/时间项/下拉选框项/文件上传项
                                                  ###富文本模块
                                   Dict[str,bool], ### 表单模块-布尔值项
                                   Dict[str,float], ### 表单模块-数字项
                                   Dict[str,List[str]], ### 表格模块-文本列/日期列/时间列/文件上传列/下拉选框列
                                   Dict[str,List[float]], ### 表格模块-数字列
                                   Dict[str,List[bool]], ### 表格模块-布尔值列
                                   List[Dict[str,str]], ### 图片集模块
                                   None
                                   ]
                             ) -> None:
        self.module_name = module_name
        self.module_type = module_type
        self.module_data = module_data
        self.type_dict = {
                          str:"文本项",
                          bool:"布尔值项",
                          float:"数字项",
                          List[str]:"文本列",
                          List[float]:"数字列",
                          List[bool]:"布尔值列"
                          }
    
    @property
    def name(self):
        return self.module_name

    @property
    def type(self):
        if self.module_type not in ["form","table","images","richtext","echarts"]:
            raise TypeError("模块类型应为“表单”、“表格”、“图片”、“富文本”和“图表”！")
        return self.module_type
    
    @property
    def data(self):
        #if self.module_type not in ["richtext","echarts"]:
        #    return None
        #else:
        return self.module_data
    
    @property
    def out(self):
        if self.data is None:
            return {
                    "name":self.name,
                    "type":self.type
                    }
        else:
            return {
                    "name":self.name,
                    "type":self.type,
                    "data":self.data
                    }
    
    def add(self,
            entry_data:Union[str, ### 表单模块-文本项/多行文本项/日期相/时间项/下拉选框项/文件上传项
                                  ###富文本模块
                             bool, ### 表单模块-布尔值项
                             float, ### 表单模块-数字项
                             List[str], ### 表格模块-文本列/日期列/时间列/文件上传列/下拉选框列
                             List[float], ### 表格模块-数字列
                             List[bool], ### 表格模块-布尔值列
                             Dict[str,str], ### 图片集模块
                             None],
            entry_name:str = None
            ):
        if self.type != "images":
            if entry_name is None:
                entry_name = str(datetime.datetime.now())
                if type(entry_data) in self.type_dict.keys():
                    entry_name = self.type_dict[type(entry_data)] + entry_name
            self.data[entry_name] = entry_data
        else:
            self.data.append(entry_data)

class eln_form_Module(eln_Module):
    """表单模块"""
    def __init__(self, 
                 module_name: str, 
                 module_data:Union[
                                   Dict[str,str], ### 表单模块-文本项/多行文本项/日期相/时间项/下拉选框项/文件上传项
                                   Dict[str,bool], ### 表单模块-布尔值项
                                   Dict[str,float], ### 表单模块-数字项
                                   None
                                   ],
                 module_type: str = "form") -> None:
        super().__init__(module_name, module_type, module_data)
        self.type_dict = {
                          str:"文本项",
                          bool:"布尔值项",
                          float:"数字项",
                          }
    
    def add(self,
            entry_data:Union[
                             str, ### 文本项/多行文本项/日期相/时间项/下拉选框项/文件上传项
                             bool, ### 布尔值项
                             float ### 数字项
                             ],
            entry_name:str = None,
            ):
        if type(entry_data) not in self.type_dict.keys():
            raise TypeError(f"表单模块只能导入文本项/多行文本项/日期相/时间项/下拉选框项/文件上传项/布尔值项/数字项而不是{type(entry_data)}")
        if entry_name is None:
            entry_name = self.type_dict[type(entry_data)] + str(datetime.datetime.now())
        self.data[entry_name] = entry_data

class eln_table_Module(eln_Module):
    """表格模块"""
    def __init__(self, 
                 module_name: str, 
                 module_data:Union[
                                   Dict[str,List[str]], ### 表格模块-文本列/日期列/时间列/文件上传列/下拉选框列
                                   Dict[str,List[float]], ### 表格模块-数字列
                                   Dict[str,List[bool]], ### 表格模块-布尔值列
                                   None
                                   ],
                 module_type: str = "table") -> None:
        super().__init__(module_name, module_type, module_data)
        self.type_dict = {
                          List[str]:"文本列",
                          List[float]:"数字列",
                          List[bool]:"布尔值列"
                          }
    
    def add(self,
            entry_data:Union[
                             List[str], ### 文本列/日期列/时间列/文件上传列/下拉选框列
                             List[float], ### 数字列
                             List[bool], ### 布尔值列
                             ],
            entry_name:str = None,
            ):
        if type(entry_data) not in self.type_dict.keys():
            raise TypeError(f"表格模块只能导入文本列/日期列/时间列/文件上传列/下拉选框列/数字列/布尔值列而不是{type(entry_data)}")
        if entry_name is None:
            entry_name = self.type_dict[type(entry_data)] + str(datetime.datetime.now())
        self.data[entry_name] = entry_data

class eln_richtext_Module(eln_Module):
    """富文本模块"""
    def __init__(self, 
                 module_name: str, 
                 module_data: Union[Dict[str,str],None], ###富文本模块 
                 module_type: str = "richtext") -> None:
        super().__init__(module_name, module_type, module_data)
    
    def add(self,
            entry_data:str, ### 文本项
            entry_name:str = None,
            ):
        if type(entry_data) != str:
            raise TypeError(f"富文本模块只能导入文本项而不是{type(entry_data)}")
        if entry_name is None:
            entry_name = self.type_dict[type(entry_data)] + str(datetime.datetime.now())
        self.data[entry_name] = entry_data

class eln_images_Module(eln_Module):
    """图片集模块"""
    def __init__(self, 
                 module_name: str, 
                 module_data: Union[List[Dict[str,str]],None], ### 图片集模块 
                 module_type: str = "images") -> None:
        super().__init__(module_name, module_type, module_data)
    
    def add(self,
            entry_data:Dict[str,str] ### 图片集模块
            ):
        self.data.append(entry_data)

class eln_data():
    """
    物理所电子实验平台数据模块基本类
    """
    def __init__(self,
                 module_name:str,
                 data,
                 data_type:str,
                 data_name:str=None,):
        self.module_name = module_name
        if data_type not in ["text","number","file","date","time","richtext","bool"]:
            raise TypeError("只能导入“文本”、“数字”、“文件”、“日期”、“时间”、“富文本”和“布尔值”！")
        self.data_type = data_type
        if data_name is None:
            self.data_name = data_type + "_" + str(datetime.datetime.now())
        else:
            self.data_name = data_name
        self.data = data
    
    @property
    def out(self):
        return {
                "module": self.module_name,
                "type": self.data_type,
                "name": self.data_name,
                "data": self.data
               }
    
class eln_text_data(eln_data):
    """文本型数据"""
    def __init__(self, 
                 module_name: str, 
                 data: str,
                 data_type: str = "text", 
                 data_name: str = None):
        super().__init__(module_name,data,data_type,data_name)
    
class eln_number_data(eln_data):
    """数字型数据"""
    def __init__(self, 
                 module_name: str, 
                 data: str,
                 data_type: Union[int,float] = "number", 
                 data_name: str = None):
        super().__init__(module_name,data,data_type,data_name)
    
class eln_file_data(eln_data):
    """文件型数据"""
    def __init__(self, 
                 module_name: str, 
                 data: str,
                 data_type: str = "file", 
                 data_name: str = None):
        super().__init__(module_name,data,data_type,data_name)

class eln_date_data(eln_data):
    """日期型数据"""
    def __init__(self, 
                 module_name: str, 
                 data: str,
                 data_type: str = "date", 
                 data_name: str = None):
        super().__init__(module_name,data,data_type,data_name)
    
class eln_time_data(eln_data):
    """时间型数据"""
    def __init__(self, 
                 module_name: str, 
                 data: str,
                 data_type: str = "time", 
                 data_name: str = None):
        super().__init__(module_name,data,data_type,data_name)
    
class eln_richtext_data(eln_data):
    """富文本型数据"""
    def __init__(self, 
                 module_name: str, 
                 data: str,
                 data_type: str = "richtext", 
                 data_name: str = None):
        super().__init__(module_name,data,data_type,data_name)
    
class eln_bool_data(eln_data):
    """布尔值型数据"""
    def __init__(self, 
                 module_name: str, 
                 data: str,
                 data_type: bool = "bool", 
                 data_name: str = None):
        super().__init__(module_name,data,data_type,data_name)
    
class eln():
    """
    物理所电子实验平台数据传输类
    """
    def __init__(self):
        self.__username = os.getenv("eln_username")
        self.__password = os.getenv("eln_password")
        self._AccessToken_url = "https://in.iphy.ac.cn/open/tokens2.php"
        self._elns_url = self.get_url('elns')
        self._search_url = self.get_url('search')
        self._import_url = self.get_url('import')
        self._export_url = self.get_url('export')
        self._update_url = self.get_url('update')
        self._headers_url = 'application/x-www-form-urlencoded'
        self._headers_json = 'application/json'
        self.module_dict = {
                            "form":eln_form_Module,
                            "table":eln_table_Module,
                            "images":eln_images_Module,
                            "richtext":eln_richtext_Module
                            }
        self.data_dict = {
                          "text":eln_text_data,
                          "number":eln_number_data,
                          "file":eln_file_data,
                          "date":eln_date_data,
                          "time":eln_time_data,
                          "richtext":eln_richtext_data,
                          "bool":eln_bool_data,
                          }

    def get_url(self,name:str)->str:
        return f"https://eln.iphy.ac.cn:61263/open_eln/eln_api_{name}.php"

    def get_AccessToken(self):
        response = requests.post(
                                 url=self._AccessToken_url,
                                 data={
                                       "username":self.__username,
                                       "password":self.__password
                                       },
                                 headers = {
                                            'Content-Type':self._headers_url,
                                            'Authorization':'refreshToken'
                                           }
                                )
        self._token = response.json()["access"]["token"]
    
    def refresh_AccessToken(self):
        if not hasattr(self,'_token'):
            self.get_AccessToken()

    def respose_status(self,response):
        errcode = response.json()['errcode']
        if errcode == 0:
            return 'OK'
        elif errcode == 1:
            raise SystemExit("认证Token信息无效!")
        elif errcode == 2:
            raise ValueError("数据格式错误!")
        elif errcode == 3:
            raise IOError("服务器原因错误!")
        elif errcode == "refresh":
            self.get_AccessToken()
            return "refresh"

    def request_url(self,
                    url:str,
                    content_type:str,
                    #is_need_data:bool = False,
                    **kwargs):
        if content_type == 'application/json':
            return requests.post(
                                 url = url,
                                 headers = {
                                            'Content-Type':content_type,
                                            'Authorization':f"Bearer {self._token}"
                                           },
                                 json = kwargs
                                 )
        else:
            return requests.post(
                                 url = url,
                                 headers = {
                                            'Content-Type':content_type,
                                            'Authorization':f"Bearer {self._token}"
                                           }
                                 )

    #@property
    def eln_list(self):
        self.eln = []
        errcode = "refresh"        
        while errcode == "refresh":
            self.refresh_AccessToken()
            response = self.request_url(
                                        url=self._elns_url,
                                        content_type=self._headers_url
                                        )
            errcode = self.respose_status(response)
        if errcode == 'OK':
            self.eln = [response.json()['my'][i]['showtext'] for i in range(len(response.json()['my']))]
            #return [response.json()['my'][i]['showtext'] for i in range(len(response.json()['my']))]
        #else:
            #self.eln = []
            #return None

    def add_module(self,
                   module_type:str,
                   module_name:str = None,
                   module_data=None) -> dict:
        if module_name is None:
            module_name = module_type + str(datetime.datetime.now())
        if module_type not in self.module_dict.keys():
            raise TypeError("只能导入“表单”、“表格”、“图片”、“富文本”和“图表”模块！")
        else:
            module = self.module_dict[module_type](module_name=module_name,
                                                   module_data=module_data)
            return module.out
    
    def add_data(self,
                 module_name:str,
                 data_type:str,
                 data,
                 data_name: str = None
                 ) -> dict:
        if data_name is None:
            data_name = module_name + data_type + str(datetime.datetime.now())
        if data_type not in self.data_dict.keys():
            raise TypeError("只能导入“文本”、“数字”、“文件”、“日期”、“时间”、“富文本”和“布尔值”！")
        else:
            data = self.data_dict[data_type](module_name=module_name,
                                             data_type = data_type,
                                             data_name = data_name,
                                             data = data)
        return data.out

    """
    def add_data(self,
                 module_name:str,
                 module_type:str,
                 data_type:str,
                 data_name:str,
                 data=None,
                 **kwargs) -> dict:
        out = {"module":module_name,"name":data_name,"type":data_type,"data":data}
        if data_type not in ["text","number","file","date","time","richtext","bool"]:
            raise TypeError("只能导入“文本”、“数字”、“文件”、“日期”、“时间”、“富文本”和“布尔值”！")
        if module_type == "table":
            if "row" in kwargs.keys():
                out["row"] = kwargs["row"]
                del out["type"]
                del out["name"]
        return out
    """

    def import_dataset(self,
                       data,
                       title:str=None,
                       keyword:str=None,
                       uid:str=None,
                       ) -> dict:
        date_now = str(datetime.datetime.now())
        out = {
                "title":date_now if title is None else title,
                "uid":date_now if uid is None else uid,
                "data":data
                }
        if keyword is not None:
            out["keyword"] = keyword
        return out

    def import_json_data(self,
                         eln_name:str,
                         template_name:str,
                         dataset_in:List[dict],
                         title_list:Union[List[dict],None]=None,
                         uid_list:Union[List[dict],None]=None,
                         keyword_list:Union[List[dict],None]=None,
                         quote:Union[List[dict],None]=None,
                         ) -> dict:

        title_list = [None] * len(dataset_in) if title_list is None else title_list
        uid_list = [None] * len(dataset_in) if uid_list is None else uid_list
        keyword_list = [None] * len(dataset_in) if keyword_list is None else keyword_list

        dataset = [self.import_dataset(data=dataset_in[i],
                                       title=title_list[i],
                                       uid=uid_list[i],
                                       keyword=keyword_list[i]) for i in range(len(dataset_in))]
        out = {
               "eln": eln_name,
               "template": template_name,
               "dataset":dataset
               }
        out["quote"] = quote if quote is not None else None
        return out 
    
    def import_data(self,
                    eln_name:str,
                    template_name:str,
                    dataset_in:List[dict],
                    title_list:Union[List[dict],None]=None,
                    uid_list:Union[List[dict],None]=None,
                    keyword_list:Union[List[dict],None]=None,
                    quote:Union[List[dict],None]=None,
                    ):
        self.refresh_AccessToken()
        if not hasattr(self,'eln'):
            self.eln_list()
        if eln_name not in self.eln:
            raise KeyError("没有该记录本！")
        elif len(dataset_in) == 0:
            raise ValueError("没有导入数据")
        else:
            response = self.request_url(
                                        url = self._import_url,
                                        content_type = self._headers_json,
                                        **self.import_json_data(
                                                                eln_name=eln_name,
                                                                title_list=title_list,
                                                                uid_list=uid_list,
                                                                keyword_list=keyword_list,
                                                                quote = quote,
                                                                template_name=template_name,
                                                                dataset_in = dataset_in
                                                                )
                                        )
            if response.status_code != 200:
                raise IOError("导入失败！")

    def export_json_data(self,
                         eln_name_list:List[str],
                         date_start:str = None,
                         date_end:str = None,
                         keywords:list = None,
                         uids:list = None) -> dict:
        out = {}
        out["eln"] = eln_name_list
        if date_start is not None:
            out["date_start"] = date_start
        if date_end is not None:
            out["date_end"] = date_end
        if keywords is not None:
            out["keywords"] = keywords
        if uids is not None:
            out["uids"] = uids
        return out

    def export_data(self,
                    eln_name_list:Union[List[str],str],
                    data_func,
                    date_start:str = None,
                    date_end:str = None,
                    keywords:list = None,
                    uids:list = None) -> dict:
        self.refresh_AccessToken()
        if not hasattr(self,'eln'):
            self.eln_list()
        if type(eln_name_list) == str:
            eln_name_list = [eln_name_list]
        for eln_name in eln_name_list:
            if eln_name not in self.eln:
                raise KeyError("没有该记录本！")
        else:
            response = self.request_url(
                                        url = self._export_url,
                                        content_type = self._headers_json,
                                        **self.export_json_data(eln_name_list=eln_name_list,
                                                                date_start=date_start,
                                                                date_end=date_end,
                                                                keywords=keywords,
                                                                uids=uids)
                                        )
            if response.status_code != 200:
                raise IOError("导出数据失败！")
            else:
                datasets = response.json()["dataset"]
                """
                datasets:List[dict]
                datasets[i]:dict=dataset
                                 dataset:{
                                          "eln_name":eln_name,
                                          "id":id,
                                          "title":title,
                                          "comm":comm,
                                          "uid":uid,
                                          "data":List[dict] 
                                                 module_data:dict=eln_Module
                                          }
                                                 module_data:{
                                                              "uid":uid,
                                                              "name":name,
                                                              "type":type,
                                                              "data":List[dict] eln_data
                                                             }
                                                                     data:dict
                                                                          {
                                                                           "uid":uid,
                                                                           "data":data,
                                                                           "name":name,
                                                                           "type":type
                                                                          }
                """
                out = {}
                for dataset in datasets:
                    out[dataset["title"]] = [data_func(pd.DataFrame(dataset["data"][i]["data"]).set_index("name")[["data","type"]]) 
                                             for i in range(len(dataset["data"]))]
                return out

    def update_json_data(self,
                         eln_name:str,
                         uid:str,
                         addModule:List[dict],
                         add:List[dict]):
        out = {
               "eln": eln_name,
               "uid": uid
               }
        if len(addModule) > 0:
            out["addModule"] = addModule
        if len(add) > 0:
            out["add"] = add
        return out

    def update_template(self,
                        module_name:str,
                        module_type:str,
                        data_func,
                        module_data=None,
                        data_in:Union[pd.DataFrame,None]=None
                        ) -> List[dict]:
        if module_type not in self.module_dict.keys():
            raise TypeError("只能导入“表单”、“表格”、“图片”、“富文本”和“图表”模块！")
        module_out = [self.module_dict[module_type](module_name=module_name,
                                                    module_data=module_data).out]
        data_in = data_func(data_in)
        data_out = []
        for i in range(len(data_in)):
            if data_in[i]["data type"] not in self.data_dict.keys():
                raise TypeError("只能导入“文本”、“数字”、“文件”、“日期”、“时间”、“富文本”和“布尔值”！")
            else:
                data_out.append(self.data_dict[data_in[i]["data type"]](module_name=module_name,
                                                                        data_name=data_in[i]["data name"],
                                                                        data=data_in[i]["data"]).out)
        return module_out,data_out

    def update_data(self,
                    eln_name:str,
                    uid:str,
                    module_name:str,
                    module_type:str,
                    data_func,
                    data_in:Union[pd.Series,None]=None):
        self.refresh_AccessToken()
        if not hasattr(self,'eln'):
            self.eln_list()
        if eln_name not in self.eln:
            raise KeyError("没有该记录本！")
        else:
            add_module, add_data = self.update_template(module_name=module_name,
                                                        module_type=module_type,
                                                        data_func=data_func,
                                                        data_in=data_in)
            response = self.request_url(
                                        url = self._update_url,
                                        content_type = self._headers_json,
                                        **self.update_json_data(
                                                                eln_name=eln_name,
                                                                uid=uid,
                                                                addModule = add_module,
                                                                add = add_data
                                                                )
                                        )
            if response.status_code != 200:
                raise IOError("导入失败！")

    def update_dataset(self,
                       eln_name:str,
                       uid:str,
                       module_name:List[str],
                       module_type:List[str],
                       data_func,
                       data_in:Union[pd.DataFrame,None]=None):
        self.refresh_AccessToken()
        if not hasattr(self,'eln'):
            self.eln_list()
        if eln_name not in self.eln:
            raise KeyError("没有该记录本！")
        else:
            if max(len(module_name),len(module_type),len(data_in)) != min(len(module_name),len(module_type),len(data_in)):
                raise TypeError("数据集长度不一样！")
            else:
                module_out, data_out = [],[]
                for i,index in enumerate(data_in.index):
                    add_module, add_data = self.update_template(module_name=module_name[i],
                                                                module_type=module_type[i],
                                                                data_func=data_func,
                                                                data_in=data_in.loc[index])
                    module_out += add_module
                    data_out += add_data
                response = self.request_url(
                                        url = self._update_url,
                                        content_type = self._headers_json,
                                        **self.update_json_data(
                                                                eln_name=eln_name,
                                                                uid=uid,
                                                                addModule = module_out,
                                                                add = data_out
                                                                )
                                        )
                if response.status_code != 200:
                    raise IOError("导入失败！")

