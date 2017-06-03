import java.util.Arrays;

/**
 * @author Yoni
 *
 */
public class JackTokenizer {
	
	
	private final String[] KEYWORDS = {"class" , "constructor" , "function" , "method" , "field" , "static" ,
										"var" , "int" , "char" , "boolean" , "void" , "true" , "false" , "null" , "this" ,
										"let" , "do" , "if" , "else" , "while" , "return" };
	
	
	public final String[] SYMBOL = {"{" , "}" , "(" , ")" , "[" , "]" , "." , "," , ";" , "+" , 
									"-" , "*" , "/" , "&" , "|" , "<" , ">" , "=" , "~"};
	
	private String currentToken, nextToken;
	
	private TokenType currentTokenType;
	
	private Parser parserJackFile;
		
	public JackTokenizer(String jackFile) 
	{
		this.parserJackFile = new Parser(jackFile);
		this.nextToken = parserJackFile.getFirstToken();
		this.currentToken = null;
		this.currentTokenType = null;
	}
	


	public boolean hasMoreTokens()
	{
		return this.nextToken != null; 
	}
	
	public void advance()
	{
		this.currentToken = this.nextToken;
		this.nextToken = getCurrentToken();
	}
	
	public TokenType tokenType()
	{
		
		if (this.currentToken == null)
			return currentTokenType;
		
		if(this.currentToken.charAt(0) == '@')
			currentTokenType = TokenType.STRING_CONST;
		
		else if (Arrays.asList(KEYWORDS).contains(this.currentToken))
			currentTokenType = TokenType.KEYWORD;
		
		else if (Arrays.asList(SYMBOL).contains(this.currentToken))
			currentTokenType = TokenType.SYMBOL;
		
		else if (this.currentToken.matches("[0-9]+"))
			currentTokenType = TokenType.INT_CONST;
				
		else 
			currentTokenType = TokenType.IDENTIDIER;
			
		return currentTokenType;
	}
	
	private String getCurrentToken()
	{
		return parserJackFile.getValueToken();
	}
	
	private void errorTokenType(TokenType expectedTokenType)
	{
		if (this.currentTokenType != expectedTokenType){
			System.err.println("Error: the token: " + currentToken + 
					"is not of type" + this.currentTokenType.toString());
		}
	}
	
	public KeyWord keyWord()
	{
		if (this.currentTokenType != TokenType.KEYWORD)
			errorTokenType(TokenType.KEYWORD);
		 
		return KeyWord.getKeyWordType(currentToken);		
	}
	
	public char symbol()
	{
		if (this.currentTokenType != TokenType.SYMBOL)
			errorTokenType(TokenType.SYMBOL);
		
		return currentToken.charAt(0);	

	}
	
	public String identifier()
	{
		if (this.currentTokenType != TokenType.IDENTIDIER)
			errorTokenType(TokenType.IDENTIDIER);
		
		return currentToken;
	}
	
	public int intVal()
	{
		if (this.currentTokenType != TokenType.INT_CONST)
			errorTokenType(TokenType.INT_CONST);
			
		return Integer.valueOf(currentToken);
	}
	
	public String stringVal()
	{
		if (this.currentTokenType != TokenType.STRING_CONST)
			errorTokenType(TokenType.STRING_CONST);
		
		return currentToken.substring(1);
	}

}
