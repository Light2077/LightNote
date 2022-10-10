https://blog.csdn.net/qq_33459369/article/details/124449353

语法

```sql
CREATE [OR REPLACE] FUNCTION function_name (arguments)
RETURNS return_datatype AS $variable_name$  
  DECLARE  
    declaration;  
    [...]  
  BEGIN  
    < function_body >  
    [...]  
    RETURN { variable_name | value }  
  END;  $variable_name$ LANGUAGE plpgsql;

```

