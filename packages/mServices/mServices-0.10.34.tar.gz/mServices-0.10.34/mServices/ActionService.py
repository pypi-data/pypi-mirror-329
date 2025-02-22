import QueryBuilderService as QueryBuilderService
import ResponseService as ResponseService

class ActionService:
    @staticmethod
    def getAction(entity, action):
        data = QueryBuilderService("actions")\
                .where("entity",entity) \
                .where("action",action) \
                .first()
        
        return data
                