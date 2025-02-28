import pymongo

class MongoDBHelper:
    def __init__(self, host='localhost', port=27017, db_name='InformationSystem'):
        """
        初始化 MongoDB 客户端和数据库

        :param host: MongoDB 服务器主机名，默认为 'localhost'
        :param port: MongoDB 服务器端口号，默认为 27017
        :param db_name: 数据库名称，默认为 'InformationSystem'
        """
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[db_name]

    def check_attribute_exists(self, collection_name,attribute_name, attribute_value):
        """
        检查某个属性值是否已经存在于数据库中
        :param attribute_name: 属性名
        :param attribute_value: 属性值
        :return: 如果存在返回True，否则返回False
        """
        query = {attribute_name: attribute_value}
        collection = self.db[collection_name]
        result = collection.find_one(query)
        return result is not None
    
    def insert_exists(self,collection_name, data):
        """
        如果数据中的某个属性值不存在于数据库中，则插入数据
        :param data: 要插入的数据（字典形式）
        
        :return: 如果插入成功返回插入的文档的ID，否则返回None
        """
        collection = self.db[collection_name]

        result = collection.insert_one(data)
        return result.inserted_id
        #else:
         #   return None

    def find_data(self, collection_name, query={}):
        """
        从指定集合中查找数据

        :param collection_name: 集合名称
        :param query: 查询条件，默认为空字典，表示查找所有数据
        :return: 符合条件的数据列表
        """
        collection = self.db[collection_name]
        return list(collection.find(query))

    def update_data(self, collection_name, query, new_data):
        """
        更新指定集合中符合条件的数据

        :param collection_name: 集合名称
        :param query: 查询条件
        :param new_data: 要更新的数据
        :return: 更新操作的结果
        """
        collection = self.db[collection_name]
        return collection.update_many(query, {'$set': new_data})

    def delete_data(self, collection_name, query):
        """
        从指定集合中删除符合条件的数据

        :param collection_name: 集合名称
        :param query: 查询条件
        :return: 删除操作的结果
        """
        collection = self.db[collection_name]
        return collection.delete_many(query)
    def get_jiuyan_new_time(self):
        collection = self.db['JiuYan']

        # 对日期字符串进行排序并取最新的日期记录
        latest_date_document = collection.find().sort("dateField", -1).limit(1)
        # 遍历结果（虽然只有一条记录）
        for doc in latest_date_document:
            return doc['time']
        
    def add_tag_if_target_exists_and_tag_not_exists(self,target_value, new_tag, collection_name='your_collection'):
        try:
            # 选择集合
            collection = self.db[collection_name]

            # 更新文档
            result = collection.update_one(
                {
                    'target': target_value,
                    'tag': {'$exists': False}
                },
                {
                    '$set': {'tag': [new_tag]}
                }
            )

            # 检查是否有文档被更新
            if result.modified_count > 0:
                print('Tag added successfully')
                return True
            else:
                #print('No document was updated')
                return False
        except Exception as e:
            #print(f"An error occurred: {e}")
            return False



    def close_connection(self):
        """
        关闭 MongoDB 连接
        """
        self.client.close()


