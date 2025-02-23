from django.db import connection

class QueryBuilderService:
    def __init__(self, table):
        self.table = table
        self.select_columns = '*'
        self.conditions = []
        self.or_conditions = []
        self.order_by = ''
        self.limit = None
        self.offset = None
        self.group_by = ''

    def select(self, *columns):
        """Select specific columns for the query."""
        self.select_columns = ', '.join(columns) if columns else '*'  # Keep * if no columns are provided
        return self

    def where(self, column, value, operator="="):
        """Apply a WHERE condition."""
        self.conditions.append((f"{column} {operator} %s", [value]))
        return self
    
    def where_group(self, callback):
        """Encapsulates multiple OR conditions inside parentheses."""
        # Start the group
        group_conditions = []
        
        # Apply conditions inside the group using the callback
        callback(group_conditions)  # This should add conditions
        
        # Close the group
        self.conditions.append(("(" + " OR ".join([cond[0] for cond in group_conditions]) + ")", [val for cond in group_conditions for val in cond[1]]))
        return self

    def orWhere(self, column, value, operator="="):
        """Apply an OR WHERE condition."""
        self.or_conditions.append((f"{column} {operator} %s", [value]))
        return self

    def whereIn(self, column, values):
        """Filter results where column value is in a list."""
        placeholders = ', '.join(['%s'] * len(values))
        self.conditions.append((f"{column} IN ({placeholders})", values))
        return self

    def whereNotIn(self, column, values):
        """Filter results where column value is not in a list."""
        placeholders = ', '.join(['%s'] * len(values))
        self.conditions.append((f"{column} NOT IN ({placeholders})", values))
        return self
    
    def whereBetween(self, column, start, end):
        """Filter results where column value is between two values."""
        self.conditions.append((f"{column} BETWEEN %s AND %s", [start, end]))
        return self
    
    def whereLike(self, columns, search_string):
        """Apply a LIKE condition for multiple columns (search functionality)."""
        like_conditions = [f"{col} LIKE %s" for col in columns]
        self.conditions.append((f"({' OR '.join(like_conditions)})", [f"%{search_string}%"] * len(columns)))
        return self
    
    def whereNull(self, column):
        """Filter records where a column is NULL."""
        self.conditions.append((f"{column} IS NULL", None))
        return self

    def whereNotNull(self, column):
        """Filter records where a column is NOT NULL."""
        self.conditions.append((f"{column} IS NOT NULL", None))
        return self

    def count(self):
        """Get the count of records."""
        return self.aggregate("COUNT(*)")

    def max(self, column):
        """Get the max value of a column."""
        return self.aggregate(f"MAX({column})")

    def min(self, column):
        """Get the min value of a column."""
        return self.aggregate(f"MIN({column})")

    def avg(self, column):
        """Get the average value of a column."""
        return self.aggregate(f"AVG({column})")

    def aggregate(self, agg_function):
        """Helper method to execute an aggregate function."""
        query, values = self.build_query(select_column=agg_function)
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            return cursor.fetchone()[0]
        
    def pluck(self, column):
        """Get a list of values for a single column."""
        query, values = self.build_query(select_column=column)
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            return [row[0] for row in cursor.fetchall()]
        
    def orderBy(self, column, direction="asc"):
        """Apply ORDER BY sorting."""
        self.order_by = f"ORDER BY {column} {direction.upper()}"
        return self

    def first(self):
        """Retrieve the first matching record."""
        self.limit = 1  # Set limit to 1 to fetch only one record
        query, values = self.build_query()  # Build the query
        print(f"Executing query: {query}")
        
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
        return None  # Return None if no record is found
    
    def apply_conditions(self, filter_json, allowed_filters, search_string, search_columns):
        """Apply conditions based on filter_json."""
        for column, cond in filter_json.items():
            if column in allowed_filters:
                # Skip if the column already has a condition
                if not any(existing_cond[0].startswith(f"{column} ") for existing_cond in self.conditions):
                    condition = self._apply_filter_condition(column, cond)
                    if condition:
                        self.conditions.append(condition)

        # If search string is provided, add search conditions to specific columns
        if search_string and search_columns:
            # Create a group for OR conditions
            self.where_group(lambda group_conditions: [
                group_conditions.append((f"{col} LIKE %s", [f"%{search_string}%"])) for col in search_columns
            ])

        return self
    
    def _apply_filter_condition(self, column, cond):
        """Helper method to construct conditions from the filter."""
        operator = cond["o"]
        value = cond["v"]
        if operator == "LIKE":
            return f"{column} LIKE %s", [f"%{value}%"]
        elif operator == "=":
            return f"{column} = %s", [value]
        # Add more operators as needed
        return None

    def paginate(self, page, limit, allowed_sorting_columns, sort_by, sort_dir):
        """Apply pagination and sorting to the query."""
        
        # Ensure sorting is valid
        if sort_by not in allowed_sorting_columns:
            sort_by = "id"  # Default column
        
        sort_dir = sort_dir.lower() if sort_dir and sort_dir.lower() in ["asc", "desc"] else "asc"

        # Apply sorting
        self.order_by = f"ORDER BY {sort_by} {sort_dir}"

        # Calculate offset for pagination
        offset = (page - 1) * limit
        self.limit = limit
        self.offset = offset

        query, values = self.build_query()  # Build the query

        print(f"Executing query: {query}")
        print(f"Executing values: {values}")
        
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        return results
    
    def build_query(self):
        """Construct the SQL query dynamically and execute it immediately."""
        
        if self.select_columns:
            select_clause = self.select_columns  # Use the select_columns directly
        else:
            select_clause = "*"  # Default to "*" if no columns provided or it's empty

        query = f"SELECT {select_clause} FROM {self.table}"
        values = []

        # Apply WHERE conditions
        if self.conditions:
            condition_strings = []
            for cond in self.conditions:
                if isinstance(cond, tuple) and len(cond) == 2:
                    condition_strings.append(cond[0])  # SQL condition
                    values.extend(cond[1])  # Add values for WHERE conditions
                elif isinstance(cond, str):
                    condition_strings.append(cond)  # Handles "(" and ")"

            if condition_strings:
                query += " WHERE " + " AND ".join(condition_strings)

        # Apply GROUP BY
        if self.group_by:
            query += f" GROUP BY {self.group_by}"

        # Apply ORDER BY
        if self.order_by:
            query += f" {self.order_by}"

        # Apply LIMIT and OFFSET
        if self.limit is not None:
            query += f" LIMIT {self.limit}"
            if self.offset is not None:
                query += f" OFFSET {self.offset}"

        return query, values  # Returns query and values separately for parameterized execution

    def execute(self, query, values):
        """Execute the built query and return results."""
        print(f"Executing query: {query}")
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results