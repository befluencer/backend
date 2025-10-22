from dreema.orm.events import EventsInterface
from dreema.helpers.configurations import Json
from dreema.responses import SysCodes, SysMessages

"""
    
    Use: 
        Builds queries for mysql
"""


class QueryBuilder:

    def __init__(self, table: str) -> None:
        self.table = table
        self.validOps = [">", "=", "!=", "<", "<=", ">=", "<=>"]
        self.booleans = [
            "or",
            "and",
        ]

    def deleteQueryBuilder(self, filters=None, params=None):
        """
        This builder is used to build the filters to be parsed for deleting into mysql

        Parameters:
                dict (filter): The filters to be queried
                dict (params): Extra parameters added

        Returns:
            json (dict): a json serialized result containing message, status, data, trace
        """

        # process your filters
        values = []
        try:
            if filters is None and params.get("limit") == 0:
                self.query = f"delete from {self.table}"
            else:
                self.query = f"delete from {self.table} where "
                for index, (key, val) in enumerate(filters.items(), start=1):
                    column, operator, value, bool = key, "=", None, "and"

                    value = val.get("value", None) if isinstance(val, dict) else val
                    operator = val.get("op", "=") if isinstance(val, dict) else "="
                    bool = (
                        val.get("bool", "and").lower()
                        if isinstance(val, dict)
                        else "and"
                    )

                    # validate the columns, operator
                    if (
                        operator not in self.validOps
                        or bool.lower() not in self.booleans
                    ):
                        return Json(
                            {
                                "data": None,
                                "status": SysCodes.DELETE_FAILED,
                                "message": SysMessages.DELETE_FAILED,
                                "trace": f"Operator or boolean not accepted",
                            }
                        )

                    self.query += (
                        f' { bool if index > 1 else "" } {column} {operator} %s '
                    )
                    values.append(value)

                # now add the parameters
                if params and params.get("limit") != 0:
                    self.query += f" limit {params.get('limit')}"

            # Convert params to a tuple
            return Json(
                {
                    "data": {"query": self.query, "queryParams": tuple(tuple(values))},
                    "status": SysCodes.DELETE_SUCCESS,
                    "message": SysMessages.DELETE_SUCCESS,
                }
            )

        except Exception as e:
            return Json(
                {
                    "data": None,
                    "status": SysCodes.DELETE_FAILED,
                    "message": SysMessages.DELETE_FAILED,
                    "trace": f"{type(e).__name__}: {e}",
                }
            )

    def updateQueryBuilder(self, data, filters=None, params=None):
        """
        This builder is used to build the filters to be parsed for updating into mysql

        Parameters:
                dict (data): The new data to be saved
                dict (filter): The filters to be queried
                dict (params): Extra parameters added

        Returns:
            json (dict): a json serialized result containing message, status, data, trace
        """

        # process your filters
        values = []
        try:
            self.query = f"update {self.table}"
            # set values
            for index, (key, val) in enumerate(data.items(), start=1):
                column, value = key, None
                value = val

                self.query += f" SET {column} = %s"
                values.append(value)

            if filters:
                self.query += " where "
                for index, (key, val) in enumerate(filters.items(), start=1):
                    column, operator, value, bool = key, "=", None, "and"

                    value = val.get("value", None) if isinstance(val, dict) else val
                    operator = val.get("op", "=") if isinstance(val, dict) else "="
                    bool = (
                        val.get("bool", "and").lower()
                        if isinstance(val, dict)
                        else "and"
                    )

                    # validate the columns, operator
                    if (
                        operator not in self.validOps
                        or bool.lower() not in self.booleans
                    ):
                        return Json(
                            {
                                "data": None,
                                "status": SysCodes.UPDATE_FAILED,
                                "message": SysMessages.UPDATE_FAILED,
                                "trace": f"Operator or boolean not accepted",
                            }
                        )

                    self.query += (
                        f' { bool if index > 1 else "" } {column} {operator} %s '
                    )
                    values.append(value)

            # now add the parameters
            if params:
                if params.get("limit") != 0:
                    self.query += f" limit {params.get('limit')}"

            # Convert params to a tuple
            return Json(
                {
                    "data": {"query": self.query, "queryParams": tuple(tuple(values))},
                    "status": SysCodes.UPDATE_SUCCESS,
                    "message": SysMessages.UPDATE_SUCCESS,
                }
            )

        except Exception as e:
            return Json(
                {
                    "data": None,
                    "status": SysCodes.UPDATE_FAILED,
                    "message": SysMessages.UPDATE_FAILED,
                    "trace": f"{type(e).__name__}: {e}",
                }
            )

    def readQueryBuilder(self, filters=None, params=None):
        """
        This builder is used to build the filters to be parsed for reading into mysql

        Parameters:
                dict (filter): The filters to be queried
                dict (params): Extra parameters added

        Returns:
            json (dict): a json serialized result containing message, status, data, trace
        """
        self.query = f"select * from {self.table} where "

        # process your filters
        values = []
        try:
            if filters is None:
                self.query = f"select * from {self.table}"
            else:
                for index, (key, val) in enumerate(filters.items(), start=1):
                    column, operator, value, bool = key, "=", None, "and"

                    value = val.get("value", None) if isinstance(val, dict) else val
                    operator = val.get("op", "=") if isinstance(val, dict) else "="
                    bool = (
                        val.get("bool", "and").lower()
                        if isinstance(val, dict)
                        else "and"
                    )

                    # validate the columns, operator
                    if (
                        operator not in self.validOps
                        or bool.lower() not in self.booleans
                    ):
                        return Json(
                            {
                                "data": None,
                                "status": SysCodes.READ_FAILED,
                                "message": SysMessages.READ_FAILED,
                                "trace": f"Operator or boolean not accepted",
                            }
                        )

                    self.query += (
                        f' { bool if index > 1 else "" } {column} {operator} %s '
                    )
                    values.append(value)

            # now add the parameters
            if params:
                if params.get("limit") != 0:
                    self.query += f" limit {params.get('limit')}"
            else:
                pass

            # return result
            return Json(
                {
                    "data": {"query": self.query, "queryParams": tuple(tuple(values))},
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
        This builder is used to build the filters to be parsed for creating into mysql

        Parameters:
                dict (data): The data to be saved
                dict (params): Extra parameters added

        Returns:
            json (dict): a json serialized result containing message, status, data, trace
        """
        # process your filters
        qParams = []
        try:
            #
            self.query = f"insert into {self.table} ("

            if isinstance(data, dict):
                placeholders = ""
                for index, (key, val) in enumerate(data.items(), start=1):
                    self.query += f'{key} {"," if index != len(data) else ")"}'
                    placeholders += f' {" values (" if index == 1 else ""} %s {"," if index != len(data) else ")"}'
                    qParams.append(val)
                self.query += placeholders

            else:
                if isinstance(data, list):
                    for count, one in enumerate(data, start=1):
                        if count == 1:
                            for index, (key, val) in enumerate(one.items(), start=1):
                                self.query += f'{key} {"," if index == 1 else ")"}'
                            self.query += " values "

                        qParams.extend(value for _, value in one.items())
                        self.query += f'( {", ".join(["%s" for i in range(len(one))])} ) {"" if count == len(data) else "," }'

            return Json(
                {
                    "data": {"query": self.query, "queryParams": tuple(qParams)},
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
