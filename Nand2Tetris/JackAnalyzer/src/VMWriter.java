import java.io.IOException;
import java.io.PrintWriter;



public class VMWriter {

	public static enum Segment{
		CONST,
		LOCAL,
		ARG,
		STATIC,
		THIS,
		THAT,
		POINTER,
		TEMP;
		
		public Segment getTypeByName(String segment){
			if (segment.equals("const"))
				return CONST;
			
			else if (segment.equals("local"))
				return LOCAL;

			if (segment.equals("arg"))
				return ARG;
			
			else if (segment.equals("static"))
				return STATIC;
			
			else if (segment.equals("this"))
				return THIS;

			if (segment.equals("that"))
				return THAT;
			
			else if (segment.equals("pointer"))
				return POINTER;
			
			else 
				return TEMP;
		}	
		
		public String toString()
		{
			switch(this){
				case STATIC: return "static";
				case LOCAL: return "local";
				case ARG: return "argument";
				case CONST: return "constant";
				case THIS: return "this";
				case THAT: return "that";
				case POINTER: return "pointer";
				default: return "temp";
			}
		}
	}
	
	public static enum Command{
		ADD,
		SUB,
		NEG,
		EQ,
		GT,
		LT,
		AND,
		OR,
		NOT,
		NONE;
		
		public static Command getTypeByName(char command){
			if (command == '+')
				return ADD;
			
			else if (command == '-')
				return SUB;
	
			else if (command == '=')
				return EQ;
			
			else if (command == '>')
				return GT;

			if (command == '<')
				return LT;
			
			else if (command == '&')
				return AND;
			
			else if (command == '|')

				return OR;
			else{
				System.err.println("doesn't exists such binary op");
				return NONE;
			}
		}	
		
		public String toString()
		{
			switch(this){
				case ADD: return "add";
				case SUB: return "sub";
				case NEG: return "neg";
				case EQ: return "eq";
				case GT: return "gt";
				case LT: return "lt";
				case AND: return "and";
				case OR: return "or";
				default: return "not";
			}
		}
	}
	
	private PrintWriter compiledFile;
	
	public VMWriter(String compiledPathFile)
	{
		try
		{
			this.compiledFile = new PrintWriter(compiledPathFile);
			
		}catch(IOException e)
		{
			System.err.println("Error: can't creat output file");
		}
	}
	
	
	public void writePush(Segment segment, int pointer)
	{
		compiledFile.println("push "+segment.toString()+" "+String.valueOf(pointer));
	}
	
	public void writePop(Segment segment, int pointer)
	{
		compiledFile.println("pop "+segment.toString()+" "+String.valueOf(pointer));
	}
	
	public void writeCommand(Command command)
	{
		compiledFile.println(command.toString());
	}
	
	public void writeLabel(String label)
	{
		compiledFile.println("label "+label.toString());
	} 
	
	public void writeGoto(String label)
	{
		compiledFile.println("goto "+label.toString());
	} 
	
	public void writeIf(String label)
	{
		compiledFile.println("if-goto "+label.toString());
	} 
	
	public void writeFunction(String name, int nLocals)
	{
		compiledFile.println("function "+name+" "+String.valueOf(nLocals));
	} 
	
	public void writeCall(String name, int nArgs)
	{
		compiledFile.println("call "+name+" "+String.valueOf(nArgs));
	} 
	
	public void writeReturn()
	{
		compiledFile.println("return");
	} 
	
	public void close()
	{
		compiledFile.close();
	} 
	
	
	
	
	
	
}
