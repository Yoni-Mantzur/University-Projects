
public enum TokenType {
	KEYWORD,
	SYMBOL,
	IDENTIDIER,
	INT_CONST,
	STRING_CONST;
	
	@Override
	public String toString()
	{
		switch(this){
			case KEYWORD: return "keyword";
			case SYMBOL: return "symbol";
			case IDENTIDIER: return "identifier";
			case INT_CONST: return "integerConstant";
			case STRING_CONST: return "stringConstant";
			default: return "NON TYPE";
		}
	}
}
