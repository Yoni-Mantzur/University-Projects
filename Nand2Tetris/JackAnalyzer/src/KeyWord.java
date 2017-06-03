
public enum KeyWord {
	CLASS, 
	METHOD,
	FUNCTION,
	CONSTRUCTOR, 
	INT,
	BOOLEAN, 
	CHAR, 
	VOID,
	VAR, 
	STATIC, 
	FIELD,
	LET, 
	DO, 
	IF, 
	ELSE,
	WHILE, 
	RETURN, 
	TRUE,
	FALSE, 
	NULL, 
	THIS,
	NON_TYPE;	
	
	@Override
	public String toString()
	{
		switch(this){
			case CLASS: return "class";
			case METHOD: return "method";
			case FUNCTION: return "function";
			case CONSTRUCTOR: return "constructor";
			case INT: return "int";
			case BOOLEAN: return "boolean";
			case CHAR: return "char";
			case VOID: return "void";
			case STATIC: return "static";
			case FIELD: return "field";
			case LET: return "let";
			case DO: return "do";
			case IF: return "if";
			case VAR: return "var";
			case ELSE: return "else";
			case WHILE: return "while";
			case RETURN: return "return";
			case TRUE: return "true";
			case FALSE: return "false";
			case NULL: return "null";
			case THIS: return "this";
			default: return "non type";
		}
	}
	
	
	public static KeyWord getKeyWordType(String keyWord)
	{
		if (keyWord.equals("class"))
			return CLASS;
		
		if (keyWord.equals("constructor"))
			return CONSTRUCTOR;
		
		if (keyWord.equals("function"))
			return FUNCTION;
		
		if (keyWord.equals("method"))
			return METHOD;
		
		if (keyWord.equals("field"))
			return FIELD;
		
		if (keyWord.equals("static"))
			return STATIC;
		
		if (keyWord.equals("var"))
			return VAR;
		
		if (keyWord.equals("int"))
			return INT;
		
		if (keyWord.equals("char"))
			return CHAR;
		
		if (keyWord.equals("void"))
			return VOID;
		
		if (keyWord.equals("boolean"))
			return BOOLEAN;
		
		if (keyWord.equals("true"))
			return TRUE;
		
		if (keyWord.equals("false"))
			return FALSE;
		
		if (keyWord.equals("null"))
			return NULL;
		
		if (keyWord.equals("this"))
			return THIS;
		
		if (keyWord.equals("let"))
			return LET;
		
		if (keyWord.equals("do"))
			return DO;
		
		if (keyWord.equals("if"))
			return IF;
		
		if (keyWord.equals("else"))
			return ELSE;
		
		if (keyWord.equals("while"))
			return WHILE;
		
		if (keyWord.equals("return"))
			return RETURN;
		
		return NON_TYPE;		
	}
}
