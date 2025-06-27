from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient
from typing import Optional
import json
from lmlib.utils import singleton
from sqlglot import Tokenizer, TokenType, parse_one, exp


@singleton
class AzureDigitalTwinClient:
    """ Class for interacting with the Azure Digital Twins client. """

    def __init__(self, adt_endpoint: str, credential: Optional[DefaultAzureCredential] = None):
        """
        Singleton class for initializing the DtClient with configuration and credentials.

        :param credential: Azure credentials for authentication (DefaultAzureCredential if None).
        """
        self.credential = credential or DefaultAzureCredential()
        self.adt_endpoint = adt_endpoint
        self.client = self._create_client()

    def _create_client(self) -> DigitalTwinsClient:
        """ Creates and returns a DigitalTwinsClient instance. """
        return DigitalTwinsClient(self.adt_endpoint, self.credential)



@singleton
class AzureDigitalTwinMockClient:
    def __init__(self, twin_graph):
        with open(twin_graph) as f:
            self.digital_twin = json.load(f)
    
    def list_models(self):
        return self.digital_twin["digitalTwinsModels"]
    
    def get_model(self, model_id):
        result =  [item for item in self.digital_twin['digitalTwinsModels'] if item["@id"]== model_id]
        if result:
            return result.pop()
        else:
            return {}
        
    def decommission_model(self, model_id):
        raise AttributeError("Decommissioning model is not supported on Mock DT") 
    
    def delete_model(self, model_id: str):
        raise AttributeError("Model deletion is not supported on Mock DT")
    
    def upsert_digital_twin(self, twin_id: str, twin_data: dict):
        raise AttributeError("Model creation is not supported on Mock DT")
    
    def get_digital_twin(self, twin_id: str):
        result = [item for item in self.digital_twin['digitalTwinsGraph']['digitalTwins'] if item['$dtId'] == twin_id]
        if result:
            return result.pop()
        else:
            return {}


    def query_twins(self, query_expression: str):
        ## known : 
        #   1. table name is always source  and/or target
        #   2. if JOIN exists then source and target exist and the query is based on filtering on relationships and twin id (call list_relationships / list_incoming_relationships)
        #   3. If both source and target exist then relation between source and target is followed by RELATED keyword
        #   4. If both source and target exist then the filter criteria is either on source or target and follows the  WHERE Keyword
        #   5. If JOIN does not exists then the query os based on filtering on twin id (call get_digital_twin)

        tokens = Tokenizer().tokenize(query_expression)
        token_values = [token.text.lower() for token in tokens]
        is_join_query = False
        frm_relation = False
        to_relation = False
        identifier = str()
        literal = str()
        join_tokens = list(filter(lambda token: token.token_type ==  TokenType.JOIN, tokens))
        var_tokens =  list(filter(lambda token: token.token_type ==  TokenType.VAR, tokens))
        where_token = list(filter(lambda token: token.token_type ==  TokenType.WHERE, tokens))
        eq_token = list(filter(lambda token: token.token_type ==  TokenType.EQ, tokens))
        is_model_of_query = False
        if "is_of_model" in token_values:
           is_model_of_query = True

            
        from_idx = -1
        for idx, token in enumerate(tokens):
            if token.token_type == TokenType.FROM:
                from_idx = idx
        assert(from_idx > -1)

        sub_query = query_expression[:tokens[from_idx+1].end+1]

        column_names = [column.alias_or_name for column in parse_one(sub_query).find_all(exp.Column)]

        #table_names = [table for table in  parse_one(sub_query).find_all(exp.Table)]

        
    
        print(column_names)

        #print(table_names)    
        # select_filters = [("source","*"), ("target", "*")]
        # if column_names:
        #      select_filters = [(table, field) for name in column_names for table, field in name.split(".") ]
        
        if join_tokens:
            is_join_query = True
            related_token= filter(lambda token: token.text == "related" , var_tokens)
            if not related_token:
                raise ValueError("Query Parsing Failed, A JOIN query should have the RELATED keyword")
            related_index = token_values.index("related")
            s = tokens[related_index + 1]
            dot = tokens[related_index + 2]
            relation = tokens[related_index + 3]
            print(relation.token_type)
            assert(s.token_type == TokenType.VAR)
            assert(dot.token_type == TokenType.DOT)
            try:
                assert(relation.token_type == TokenType.VAR)
            except:    
                assert(relation.token_type == TokenType.WITH)
            if s.text == "source":
               frm_relation = True
            elif s.text == "target":
                to_relation = True
            else:
                raise AttributeError("Query should have source / target as identifier")
            relation_name = relation.text
        if not where_token:
            raise AttributeError("No filter query provided")    
        where_index = token_values.index("where")
        if eq_token:
            s = tokens[where_index + 1]
            dot = tokens[where_index + 2]
            identifier = tokens[where_index + 3]
            operator = tokens[where_index + 4]
            expression = tokens[where_index + 5]
            assert(s.token_type == TokenType.VAR)
            assert(dot.token_type == TokenType.DOT)
            assert(identifier.token_type == TokenType.VAR)
            assert(operator.token_type == TokenType.EQ)
            assert(expression.token_type == TokenType.STRING)
            assert(identifier.text == "$dtId")
            twin_id = expression.text      
            print(twin_id)
        if is_join_query:
            print(relation_name)
            print(frm_relation)
            print(to_relation)
            if frm_relation:
                res = []
                relations = self.list_relationships(twin_id, relation_name)
                for i in relations:
                    res.append({
                    "source": self.get_digital_twin(i['$sourceId']),
                    "target": self.get_digital_twin(i['$targetId'])
                    })
                return res
            elif to_relation:
                res = []
                relations = self.list_incoming_relationships(twin_id, relation_name)
                for i in relations:
                    res.append({
                    "source": self.get_digital_twin(i['$sourceId']),
                    "target": self.get_digital_twin(i['$targetId'])
                    })
                return res
            else:
                return 
            
        elif eq_token:                       
            return [self.get_digital_twin(twin_id)]
        elif is_model_of_query:
            is_model_of_index = token_values.index("is_of_model")
            s = tokens[is_model_of_index + 1]
            assert(s.token_type == TokenType.L_PAREN)
            m = tokens[is_model_of_index + 2]
            assert(m.token_type == TokenType.STRING)
            r = tokens[is_model_of_index + 3]
            assert(r.token_type == TokenType.R_PAREN)
            print(f"model: {m.text}")
            return self.get_twins_by_model(m.text)
        else:
            return []
    

    def delete_digital_twins(self, twin_id: str):
        raise AttributeError("Deletion  is not supported on Mock DT")
    
    def update_component(self, digital_twin_id: str, component_name: str, patch: list):
        raise AttributeError("Update  is not supported on Mock DT")

    def get_component(self, digital_twin_id: str, component_name: str):
        result = [(component_name,item[component_name]) for item in self.digital_twin['digitalTwinsGraph']['digitalTwins'] if item['$dtId'] == digital_twin_id and component_name in item.keys()]
        if result:
            return dict(result.pop())
        else:
            return {}
    
    def update_component(self, digital_twin_id: str, component_name: str):
        raise AttributeError("Update  is not supported on Mock DT")

    def delete_relationship(self, source_id : str,relationship_id:str):
        raise AttributeError("Delete relationship not possible on MockDT")
    
    def upsert_relationship(self, source_id: str, relationship_id: str, relationship_data: dict):
        raise AttributeError("Upsert relationship not possible on MockDT")

    def list_relationships(self, digital_twin_id, relation_filter = None):
        if not relation_filter:
            result =  [item for item in self.digital_twin['digitalTwinsGraph']['relationships'] if item['$sourceId'] == digital_twin_id]
        else:
            result =  [item for item in self.digital_twin['digitalTwinsGraph']['relationships'] if item['$sourceId'] == digital_twin_id and item['$relationshipName'] == relation_filter]
        for item in result:
            yield item
        
    def list_incoming_relationships(self, digital_twin_id, relation_filter = None):
        if not relation_filter:
            result = [item for item in self.digital_twin['digitalTwinsGraph']['relationships'] if item['$targetId'] == digital_twin_id]
        else:
           result = [item for item in self.digital_twin['digitalTwinsGraph']['relationships'] if item['$targetId'] == digital_twin_id and item['$relationshipName'] == relation_filter] 
        for item in result: 
            item["relationship_name"] = item['$relationshipName'] 
            item["source_id"] = item["$sourceId"]
            item["target_id"] = item["$targetId"]
        for item in result:
            yield item

    def list_event_routes(self):
        raise AttributeError("List event route  not possible on MockDT")

    def delete_event_routes(self, event_route_id: str):
        raise AttributeError("Delete event route relationship not possible on MockDT")

    def get_twins_by_model(self, model: str, limit = 10):
        result = list(filter(lambda item: item['$metadata']['$model'] == model ,self.digital_twin['digitalTwinsGraph']['digitalTwins']))
        for item in result:
           
            yield item


