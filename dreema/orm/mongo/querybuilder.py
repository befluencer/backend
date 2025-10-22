from dreema.helpers import Json
from dreema.responses import SysCodes, SysMessages
from bson import ObjectId

"""
    
    Use: 
        Query Builder compiles all database queries into a structure
        and secured form to be executed by the queries class
"""


class QueryBuilder:
    def __init__(self, table: str) -> None:
        """
        initializes class parameters to be used for further processing
        """
        self.table = table
        self.validOps = [
            ">",
            "=",
            "!=",
            "<",
            "<=",
            ">=",
            "in"
            "nin",
        ]
        self.validOpsMap = {
            ">": "$gt",
            "=": "$eq",
            "!=": "$ne",
            "<": "$lt",
            "<=": "$lte",
            ">=": "$gte",
            "in": "$in",
            "nin": "$nin",
        }
        self.booleans = [
            "OR",
            "AND",
        ]
        self.booleanMap = {"OR": "$or", "AND": "$and"}
 
  
    def readQueryBuilder(self, filters=None, params=None):
        """
        This builder sets the filters in the right format
        to be parsed for read database operation
        Same builder is employed delete and update since they both require some reading

        Parameters:
                dict (filters): Takes the query filters passed from the controller
                dict (params): Extra parameters added

        Returns:
            json (dict): a json serialized result containing message, status, data, trace

        """

        self.query = {}

        # process your filters
        try:
            if filters is not None:
                op = self.booleanMap.get(('and' if not params else params.get('bool','and')).upper())
                self.query = {op: []}
                for key, val in filters.items():

                    column, operator, value, logic = key, "=", None, "AND"
                    value = val.get("value", None) if isinstance(val, dict) else val
                    operator = val.get("op", "=") if isinstance(val, dict) else "="
                    logic = (
                        val.get("bool", "and").upper()
                        if isinstance(val, dict)
                        else "AND"
                    )

                    # validate the columns, operator
                    if (
                        operator not in self.validOps
                        and logic not in self.booleans
                    ):
                        return Json(
                            {
                                "data": None,
                                "status": SysCodes.READ_FAILED,
                                "message": SysMessages.READ_FAILED,
                                "trace": f"Operator or boolean not accepted",
                            }
                        )


                    if key=='_id':
                        value = ObjectId(value) if isinstance(value, str) else [ObjectId(val) for val in value]
                    operator = self.validOpsMap.get(operator)
                    logic = self.booleanMap.get(logic)
                    condition = {column: {operator: value}}

                    # Handle grouping based on the boolean
                    self.query[op].append(condition)

            return Json(
                {
                    "data": {"query": self.query},
                    "status": SysCodes.READ_SUCCESS,
                    "message": SysMessages.READ_SUCCESS,
                }
            )
        except Exception as e:
            return Json(
                {
                    "data": None,
                    "status": SysCodes.READ_FAILED,
                    "message": SysMessages.READ_FAILED,
                    "trace": f"{type(e).__name__}: {e}",
                }
            )

    def createQueryBuilder(self, data, params=None):
        """
        This builder is used to build the filters to be parsed for creating into mongodb

        Parameters:
                dict (data): The data to be inserted
                dict (params): Extra parameters added

        Returns:
            json (dict): a json serialized result containing message, status, data, trace
        """

        try:
            self.query = data
            return Json(
                {
                    "data": {"query": self.query},
                    "status": SysCodes.CREATE_SUCCESS,
                    "message": SysMessages.CREATE_SUCCESS,
                }
            )

        except Exception as e:
            return Json(
                {
                    "data": None,
                    "status": SysCodes.CREATE_FAILED,
                    "message": SysMessages.CREATE_FAILED,
                    "trace": f"{type(e).__name__}: {e}",
                }
            )
