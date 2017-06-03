/**
 * @author Yoni
 *
 */
public class CompilationEngine {
	
	private VMWriter compiledFile;
	
	private JackTokenizer jackTokeizer;
	
	private SymbolTable symbolTable;
	
	private int countLabel;
	
	String className, curFuctionName;
	
	public CompilationEngine(String jackFile, String outFile) 
	{
		this.jackTokeizer = new JackTokenizer(jackFile);
		
		this.compiledFile = new VMWriter(outFile);
		
		this.className = "";
		this.curFuctionName = "";
		
		this.countLabel = 0;
			
		this.symbolTable = new SymbolTable();
	}
	
	
	
	private String getVarType()
	{
		if (jackTokeizer.tokenType() == TokenType.IDENTIDIER) // Means type is className
			return jackTokeizer.identifier();
		
		else // Premetive type
			return jackTokeizer.keyWord().toString();
		
	}
	
	public void compileClass()
	{	
		while(jackTokeizer.hasMoreTokens())
		{
			 // Class token
			jackTokeizer.advance();
			while(jackTokeizer.tokenType() == TokenType.KEYWORD)
			{
				if (jackTokeizer.keyWord() == KeyWord.CLASS)
				{

							
					// Print class name
					jackTokeizer.advance();
					if (jackTokeizer.tokenType() != TokenType.IDENTIDIER)
						System.err.println("class name must be here");
					
					this.className = jackTokeizer.identifier();
					
					// Print class {
					jackTokeizer.advance();

					
					// Print vars of class
					jackTokeizer.advance();
					CompileClassVarDec();;
					
					// Print methods of class
					CompileSubroutine();
					
					// Print class }
					jackTokeizer.tokenType();
					
					
					// Check for new class
					jackTokeizer.advance();
									
				}
				else { // For debugging propose
					return;
				}
							
			} // End while classes
			
		} // End while tokens
		compiledFile.close();
	}
	
	
	private void compileVarDefentionList(String type, SymbolTable.Kind kind)
	{
		while (jackTokeizer.tokenType() == TokenType.SYMBOL)
		{
			if (jackTokeizer.symbol() == ',')
			{
				// Print var seperation
				
				// Print var name
				jackTokeizer.advance();
				jackTokeizer.tokenType();
				symbolTable.define(jackTokeizer.identifier(), type, kind);
				
				// check for new var name
				jackTokeizer.advance();
			}	
			else { // For debugging propose
				return;
			}
		}
	}
	
	public void CompileClassVarDec()
	{
		while(jackTokeizer.tokenType() == TokenType.KEYWORD)
		{
			if (jackTokeizer.keyWord() == KeyWord.STATIC || jackTokeizer.keyWord() == KeyWord.FIELD)
			{
				// means var type
				SymbolTable.Kind kind = SymbolTable.Kind.getTypeByName(jackTokeizer.keyWord().toString());
				
				// Print var type
				jackTokeizer.advance();
				String type = getVarType();
				
					
				// Print var name
				jackTokeizer.advance();
				jackTokeizer.tokenType();
				String name = jackTokeizer.identifier();
				symbolTable.define(name, type, kind);
				
				
				// Print vars of class
				jackTokeizer.advance();
				compileVarDefentionList(type, kind);
				
				// Print vars end line ;

				// check for new var
				jackTokeizer.advance();
			}else{
				return; // Means and of this section
			}
			
		} // End while vars
		
	}

	
	public void CompileSubroutine()
	{
		while(jackTokeizer.tokenType() == TokenType.KEYWORD)
		{
			if (jackTokeizer.keyWord() == KeyWord.CONSTRUCTOR || jackTokeizer.keyWord() == KeyWord.FUNCTION 
					|| jackTokeizer.keyWord() == KeyWord.METHOD)
			{
			
				symbolTable.startSubroutine();
				
				KeyWord subrotineType = jackTokeizer.keyWord();
				
				// Print method keyword
				if (jackTokeizer.keyWord() == KeyWord.METHOD)
					symbolTable.define("this", className, SymbolTable.Kind.ARG);

				
				// Print method return type
				jackTokeizer.advance();
				getVarType(); // No meaning to return value
					
				
				// Print method name
				jackTokeizer.advance();
				jackTokeizer.tokenType();
				this.curFuctionName = this.className + "." + jackTokeizer.identifier();
				
				
				// Print parameters (
				jackTokeizer.advance();
				jackTokeizer.tokenType();
				
				// Print parameter list
				jackTokeizer.advance();
				compileParameterList();
				
				// Print parameters )
				jackTokeizer.tokenType();
				
				// Print body of method
				
				// Print subrutine {
				jackTokeizer.advance();
				jackTokeizer.tokenType();
				
				jackTokeizer.advance();
				compileVarDec();
				
				this.compiledFile.writeFunction(curFuctionName, symbolTable.varCount(SymbolTable.Kind.VAR));
				
				if (subrotineType == KeyWord.CONSTRUCTOR)
				{
					// Allocate memory for object
					compiledFile.writePush(VMWriter.Segment.CONST, symbolTable.varCount(SymbolTable.Kind.FIELD));
					compiledFile.writeCall("Memory.alloc", 1);
					compiledFile.writePop(VMWriter.Segment.POINTER, 0);
				}
				
				else if (subrotineType == KeyWord.METHOD)
				{
					// set this object
					compiledFile.writePush(VMWriter.Segment.ARG, 0);
					compiledFile.writePop(VMWriter.Segment.POINTER, 0);
				}
				
				compileStatements();
				
				// Print subrutine }
				jackTokeizer.tokenType();
				
				
				jackTokeizer.advance();
				
			}
			else { // For debugging propose
				return;
			}
			
		} // End while methods
		
	}
	

	public void compileParameterList()
	{

		TokenType type = jackTokeizer.tokenType();
		if (type == TokenType.KEYWORD || type == TokenType.IDENTIDIER) 
		{
			SymbolTable.Kind kindArgs = SymbolTable.Kind.ARG;
			// Print var type
			String argumentType = getVarType();
				
			// Print var name
			jackTokeizer.advance();
			jackTokeizer.tokenType();
			String argumentName = jackTokeizer.identifier();
			
			symbolTable.define(argumentName, argumentType, kindArgs);
			

			jackTokeizer.advance();
			
			while (jackTokeizer.tokenType() == TokenType.SYMBOL)
			{
				if (jackTokeizer.symbol() == ',')
				{
					// Print var seperation
					
					// Print var type
					jackTokeizer.advance();
					argumentType = getVarType();
					
					// check for new var name
					jackTokeizer.advance();
					jackTokeizer.tokenType();
					argumentName = jackTokeizer.identifier();
					
					symbolTable.define(argumentName, argumentType, kindArgs);
					
					jackTokeizer.advance();
				}	
				else { 
					break;
				}
			}
		} // means end parameter list
	}
	

	public void compileVarDec()
	{
		while(jackTokeizer.tokenType() == TokenType.KEYWORD)
		{
			if (jackTokeizer.keyWord() == KeyWord.VAR)
			{

				SymbolTable.Kind kindVars = SymbolTable.Kind.VAR;
				
				// Print var 

				
				// Print var type
				jackTokeizer.advance();
				String funcVarsType = getVarType();
					
				// Print var name
				jackTokeizer.advance();
				jackTokeizer.tokenType();
				String funcVarsName = jackTokeizer.identifier();
				
				symbolTable.define(funcVarsName, funcVarsType, kindVars);
				
				// Print vars of  func
				jackTokeizer.advance();
				compileVarDefentionList(funcVarsType, kindVars);
				
				// Print vars end line ;
				jackTokeizer.tokenType();
				
				// check for new var
				jackTokeizer.advance();
			}else{
				return; // Means and of this section
			}
			
		} // End while vars
	}

	public void compileStatements()
	{
		while(jackTokeizer.tokenType() == TokenType.KEYWORD) // Statments*
		{
			if (jackTokeizer.keyWord() == KeyWord.LET)
				compileLet();
			
			else if (jackTokeizer.keyWord() == KeyWord.IF)
				compileIf();
			
			else if (jackTokeizer.keyWord() == KeyWord.WHILE)
				compileWhile();
			
			else if (jackTokeizer.keyWord() == KeyWord.DO)
				compileDo();

			else if (jackTokeizer.keyWord() == KeyWord.RETURN)
				compileReturn();
						
			else { // For debugging propose
				System.err.println("In statments: Need to be statment token but was: " + jackTokeizer.keyWord().toString());
				return;
			}
		}		
	}

	
	private VMWriter.Segment getSegmentOfvar(String varName)
	{
		SymbolTable.Kind kind = symbolTable.kindOf(varName);
		
		if (kind == SymbolTable.Kind.ARG)
			return VMWriter.Segment.ARG;
		
		if (kind == SymbolTable.Kind.VAR)
			return VMWriter.Segment.LOCAL;
		
		if (kind == SymbolTable.Kind.STATIC)
			return VMWriter.Segment.STATIC;
		
		return VMWriter.Segment.THIS;
	}
	
	private void compileSubrutineCall(String varName, char symbolAfter)
	{
		// Print method  or var name name

		// print symbol after
		int numArguments = 0;
		if (symbolAfter == '(') // Means method call
		{

			compiledFile.writePush(VMWriter.Segment.POINTER, 0);
			
			varName = className + "." + varName;
			numArguments++;
		}
		
		
		else // Means class|varname.subrutineName
		{
			jackTokeizer.advance();
			jackTokeizer.tokenType();
			
			
			String typeVar = symbolTable.typedOf(varName);
			
			if (typeVar == null) // Means Class.function
				varName += ("." + jackTokeizer.identifier());
			
			else{ // Means var.method
				VMWriter.Segment seg = getSegmentOfvar(varName);
				int index = symbolTable.indexOf(varName);
				
				// Push the var object
				compiledFile.writePush(seg, index);
				numArguments++;
				varName = symbolTable.typedOf(varName) + "." + jackTokeizer.identifier();
							
			}
			// Print (
			jackTokeizer.advance();
			jackTokeizer.tokenType();
		}
		

		jackTokeizer.advance();
		numArguments += compileExpressionList();	
		
		// Print ')'
		jackTokeizer.tokenType();
		
		compiledFile.writeCall(varName, numArguments);
	}
	
	public void compileDo()
	{	
		// Print do keyword 		

		// Print method  or var name name
		jackTokeizer.advance();
		jackTokeizer.tokenType();
		String varName = jackTokeizer.identifier();
		
		jackTokeizer.advance();
		jackTokeizer.tokenType();
		char symbol = jackTokeizer.symbol();
		
		compileSubrutineCall(varName, symbol);
		
		// Print ';'
		jackTokeizer.advance();
		jackTokeizer.tokenType();
		
		compiledFile.writePop(VMWriter.Segment.TEMP, 0);
		
		jackTokeizer.advance();
	}

	
	public void compileLet()
	{	

		// Print let keyword 
		jackTokeizer.tokenType();
		
		// Print var name 
		jackTokeizer.advance();
		jackTokeizer.tokenType();
		String varName = jackTokeizer.identifier();
		
		// Print '[' OR '='
		jackTokeizer.advance();
		jackTokeizer.tokenType();
		
		int index = symbolTable.indexOf(varName);
		if (jackTokeizer.symbol() == '['){
		
			compiledFile.writePush(getSegmentOfvar(varName), index);
			
			// Print expression
			jackTokeizer.advance();
			CompileExpression();
			
			// Print ']'
			jackTokeizer.tokenType();
			
			compiledFile.writeCommand(VMWriter.Command.ADD);
			
			// Print '='
			jackTokeizer.advance();
			jackTokeizer.tokenType();
			
			jackTokeizer.advance();
			CompileExpression();
			
			compiledFile.writePop(VMWriter.Segment.TEMP, 0);
			
			compiledFile.writePop(VMWriter.Segment.POINTER, 1);
			
			compiledFile.writePush(VMWriter.Segment.TEMP, 0);
			
			compiledFile.writePop(VMWriter.Segment.THAT, 0);
			
			
		}else{		
			jackTokeizer.advance();
			CompileExpression();
			
			compiledFile.writePop(getSegmentOfvar(varName), index);
			
		}
		// Print ';'
		jackTokeizer.tokenType();
		
				
		jackTokeizer.advance();
	}
	
	private void  printBlockStatments()
	{
		// Print '{'
		jackTokeizer.advance();
		jackTokeizer.tokenType();
	
		jackTokeizer.advance();
		compileStatements();
		
		// Print '}'
		jackTokeizer.tokenType();
		
		jackTokeizer.advance();
	}
	
	
	private void compileCondition()
	{
		// Print while keyword 
		jackTokeizer.tokenType();		
	
		// Print '('
		jackTokeizer.advance();
		jackTokeizer.tokenType();
		
		jackTokeizer.advance();
		CompileExpression();
		
		// Print ')'
		jackTokeizer.tokenType();
		
	

	}
	
	public void compileWhile()
	{
		String whileLabel  = "label" + String.valueOf(countLabel++);
		String endWhile = "label" + String.valueOf(countLabel++);
		
		compiledFile.writeLabel(whileLabel);
				
		compileCondition();
		
		compiledFile.writeCommand(VMWriter.Command.NOT);
		compiledFile.writeIf(endWhile);
		
		printBlockStatments();
		compiledFile.writeGoto(whileLabel);
		
		compiledFile.writeLabel(endWhile);
	}
	
	public void compileReturn()
	{

		// Print return
		jackTokeizer.tokenType();
		
		
		jackTokeizer.advance();
		
		if (jackTokeizer.tokenType() == TokenType.SYMBOL && jackTokeizer.symbol() == ';') // MEANS return;
		{
			// Write ;
			
			compiledFile.writePush(VMWriter.Segment.CONST, 0);
		}else{
			// Print expression
			CompileExpression();
			
			// Print ';'
			jackTokeizer.tokenType();
			
		}		

		compiledFile.writeReturn();
		
		jackTokeizer.advance();
	}
	
	public void compileIf()
	{
		String ifNotLabel  = "label" + String.valueOf(countLabel++);
		String endIf = "label" + String.valueOf(countLabel++);
		
		compileCondition();
		
		compiledFile.writeCommand(VMWriter.Command.NOT);
		compiledFile.writeIf(ifNotLabel);
		printBlockStatments();
		
		compiledFile.writeGoto(endIf);
		
		
		compiledFile.writeLabel(ifNotLabel);
		
		if (jackTokeizer.tokenType() == TokenType.KEYWORD && jackTokeizer.keyWord() == KeyWord.ELSE){
			jackTokeizer.tokenType();
			printBlockStatments();
		}
		compiledFile.writeLabel(endIf);
	}
	
	
	public void compiLeBinaryOp()
	{
		while(jackTokeizer.tokenType() == TokenType.SYMBOL) // (op term)*
		{
			char symbol = jackTokeizer.symbol();
			
			if (symbol == '+' || symbol == '-' || symbol == '*' || symbol == '/' || symbol == '&' || symbol == '|' ||
					symbol == '<' || symbol == '>' || symbol == '=')
			{
				jackTokeizer.advance();
				compileTerm();	
				
				if (symbol == '*')
					compiledFile.writeCall("Math.multiply", 2);
				
				else if (symbol == '/')
					compiledFile.writeCall("Math.divide", 2);

				else
					compiledFile.writeCommand(VMWriter.Command.getTypeByName(symbol));
			}
			else
				return;
		}	
	}
	
	
	public void CompileExpression()
	{
		
		compileTerm();
		
		compiLeBinaryOp();
				
	}
	
	public void compileTerm()
	{
		boolean isNeedAdvance = true;

		
		TokenType type = this.jackTokeizer.tokenType();
		
		if (type == TokenType.INT_CONST)
			compiledFile.writePush(VMWriter.Segment.CONST, jackTokeizer.intVal());
		
		else if (type == TokenType.STRING_CONST){
			String strConst = jackTokeizer.stringVal();
			compiledFile.writePush(VMWriter.Segment.CONST, strConst.length());
			compiledFile.writeCall("String.new", 1);
			
			int asciiChar;
			for (int i = 0; i < strConst.length(); i++){
				asciiChar = (int)strConst.charAt(i);
				compiledFile.writePush(VMWriter.Segment.CONST, asciiChar);
				compiledFile.writeCall("String.appendChar", 2); // 2 for this and new char	
			}
		}
		
		else if (type == TokenType.KEYWORD){// keyword_constant
		
			KeyWord constWord = jackTokeizer.keyWord();
			
			if (constWord == KeyWord.TRUE){
				compiledFile.writePush(VMWriter.Segment.CONST, 1);
				compiledFile.writeCommand(VMWriter.Command.NEG);
			}
			
			else if (constWord == KeyWord.FALSE || constWord == KeyWord.NULL){
				compiledFile.writePush(VMWriter.Segment.CONST, 0);
			}
			
			else if (constWord == KeyWord.THIS){
				compiledFile.writePush(VMWriter.Segment.POINTER, 0);
			}
			else{
				System.err.println("error keyword expression");
			}
			
		}
		
		else if (type == TokenType.SYMBOL)
		{
			// Print symbol
			
			if (jackTokeizer.symbol() == '-' || jackTokeizer.symbol() == '~'){ // unaryOp	
				char unaryOp = jackTokeizer.symbol();
				isNeedAdvance = false;
				jackTokeizer.advance();
				compileTerm();
				
				if (unaryOp == '-')
					compiledFile.writeCommand(VMWriter.Command.NEG);
				else
					compiledFile.writeCommand(VMWriter.Command.NOT);
		
			}else{ // Expression '('
				jackTokeizer.advance();
				CompileExpression();
				//Print ')'
			}
		}
		
		else if (type == TokenType.IDENTIDIER)
		{
			String varName = jackTokeizer.identifier();
			
			jackTokeizer.advance(); // NEEDS TO BE SYMBOL

			jackTokeizer.tokenType();
			char symbol = jackTokeizer.symbol();
			if (symbol == '[')
			{
				// Print 'varName['
				
				int index = symbolTable.indexOf(varName);
				compiledFile.writePush(getSegmentOfvar(varName), index);
				
				jackTokeizer.advance(); 
				CompileExpression();
				
				// Print ']'
				jackTokeizer.tokenType();
				compiledFile.writeCommand(VMWriter.Command.ADD);
				compiledFile.writePop(VMWriter.Segment.POINTER, 1);
				compiledFile.writePush(VMWriter.Segment.THAT, 0);
				
			}
			
			else if (symbol == '(' || symbol == '.') // Subrutine call
			{
				compileSubrutineCall(varName, symbol);
			}else{
				isNeedAdvance = false;
				// print var name
				int index = symbolTable.indexOf(varName);
				compiledFile.writePush(getSegmentOfvar(varName), index);
			}
		}
		
		if (isNeedAdvance)
			jackTokeizer.advance(); 
		


	}
	
	public int compileExpressionList()
	{
		
		int numberEXpressions = 0;
		while (jackTokeizer.tokenType() != TokenType.SYMBOL ||  jackTokeizer.symbol() != ')')
		{
			
			CompileExpression();
			numberEXpressions++;
			if (jackTokeizer.tokenType() == TokenType.SYMBOL &&  jackTokeizer.symbol() == ','){
				// Print ','
				jackTokeizer.advance();			
			}
		}
		
		return numberEXpressions;
	
	}
	

}
