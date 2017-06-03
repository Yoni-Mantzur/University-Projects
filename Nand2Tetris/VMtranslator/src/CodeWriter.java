
import java.io.IOException;
import java.io.PrintWriter;


/**
 * Translates vm code to asm code.
 * @author Yoni
 *
 */
public class CodeWriter 
{
	
	// The file to read from
	private PrintWriter asmFile;
	
	
	private final String STAT = "16";
	private final String TMP = "5";
	
	// Count the conditions labels
	private int countCond;
	
	private int countFuncCalls;
	
	private String functionName;
	
	public String fileName;
	

	
	/**
	 * Constructor.
	 * @param filePath - the path of dest file
	 * @throws IOException - loading file failed
	 */
	public CodeWriter(String filePath)
	{
		try
		{
			this.asmFile = new PrintWriter(filePath);
			this.fileName = "";
			this.functionName = "";
			writeInit();
			this.countCond = 0;
			this.countFuncCalls = 0;
			
		}catch(IOException e)
		{
			System.err.println(e.getMessage());
		}
	}
	
	
	public void setFileName(String fileName)
	{
		this.countFuncCalls=0;
		this.fileName = fileName;
	}
	/*
	 * Initialize the location of the segments.
	 */
	public void writeInit()
	{
		this.asmFile.println("@256");
		this.asmFile.println("D=A");
		this.asmFile.println("@SP");
		this.asmFile.println("M=D");
		
		
		writeCall("Sys.init", "0");
		
	}
	
	/**
	 * Writes Label in asm
	 * @param label
	 */
	public void writeLabel(String label)
	{
		this.asmFile.println("("+this.functionName+"$"+label+")");
	}
	
	public void writeLabelFuction()
	{
		this.asmFile.println("("+this.functionName+")");
	}
	
	public void writeGoToFunction(String function)
	{
		this.asmFile.println("@"+function);
		this.asmFile.println("0;JMP");	
	}
	
	public void writeIfGoTo(String label)
	{
		popFromStack("@R13");
		this.asmFile.println("@R13");
		this.asmFile.println("D=M");
		this.asmFile.println("@"+this.functionName+"$"+label);
		this.asmFile.println("D;JNE");	
	}
	
	public void writeGoTo(String label)
	{
		this.asmFile.println("@"+this.functionName+"$"+label);
		this.asmFile.println("0;JMP");	
	}
	
	private void pushReturnAdd()
	{
		this.countFuncCalls++;
		this.asmFile.println("@"+this.functionName+"$ret." +
									Integer.toString(this.countFuncCalls));
		this.asmFile.println("D=A");	
		this.asmFile.println("@R13");
		this.asmFile.println("M=D");
		pushToStack("@R13");
	}
	
	public void writeCall(String functionName, String numArgs)
	{
		pushReturnAdd();
		pushToStack("@LCL");
		pushToStack("@ARG");
		pushToStack("@THIS");
		pushToStack("@THAT");
		
		// ARG = SP - n - 5
		this.asmFile.println("@SP");
		this.asmFile.println("D=M");
		this.asmFile.println("@" + numArgs);
		this.asmFile.println("D=D-A");
		this.asmFile.println("@5");
		this.asmFile.println("D=D-A");
		this.asmFile.println("@13");
		this.asmFile.println("M=D");
		changeValOfReg("ARG", "R13");
		
		// LCL = SP
		changeValOfReg("LCL", "SP");
		
		writeGoToFunction(functionName);
		
		writeLabel("ret." + Integer.toString(this.countFuncCalls));
	}
	
	public void writeReturn()
	{
		// frame = LCL
		changeValOfReg("FRAME", "LCL");
		
		// RET = *(FRAME-5)
		setRegInRet("RET","FRAME", "5");
		
		// *ARG = pop()
		popFromStack("@R13");
		this.asmFile.println("@R13");
		this.asmFile.println("D=M");
		this.asmFile.println("@ARG");
		this.asmFile.println("A=M");
		this.asmFile.println("M=D");
		
		// SP = ARG + 1
		this.asmFile.println("@ARG");
		this.asmFile.println("D=M+1");
		this.asmFile.println("@SP");
		this.asmFile.println("M=D");

		// THAT = *(FRAME-4)
		setRegInRet("THAT","FRAME", "1");
		
		// THIS = *(FRAME-3)
		setRegInRet("THIS","FRAME", "2");
		
		// ARG = *(FRAME-2)
		setRegInRet("ARG","FRAME", "3");
		
		// LCL = *(FRAME-4)
		setRegInRet("LCL","FRAME", "4");
		
		// goto RETURN ADD
		this.asmFile.println("@RET");
		this.asmFile.println("A=M");
		this.asmFile.println("0;JMP");	
	}
	
	public void writeFunction(String functionName, String numLocals)
	{
		this.functionName = functionName;
		writeLabelFuction();
		for (int i=0; i < Integer.valueOf(numLocals); i++)
		{
			pushConstantToStack("0");
			writePushPop(CommandType.C_POP, "local", Integer.toString(i));
		}
	}
	
	private void setRegInRet(String reg, String ass, String val)
	{

		this.asmFile.println("@"+val);
		this.asmFile.println("D=A");
		this.asmFile.println("@"+ass);
		this.asmFile.println("A=M-D");
		this.asmFile.println("D=M");
		this.asmFile.println("@"+reg);
		this.asmFile.println("M=D");
	}
	

	private void changeValOfReg(String reg, String newVal)
	{
		this.asmFile.println("@"+newVal);
		this.asmFile.println("D=M");
		this.asmFile.println("@"+reg);
		this.asmFile.println("M=D");		
	}
	
	
	/*
	 * Pop the value from stack and set it in the register.
	 */
	private void popFromStack(String register)
	{
		this.asmFile.println("@SP");
		this.asmFile.println("M=M-1");
		this.asmFile.println("A=M");
		this.asmFile.println("D=M");
		
		this.asmFile.println(register);
		this.asmFile.println("M=D");
	}
	
	/*
	 * Pop the value from stack and set it in the register.
	 */
	private void popFromStack(String basePtr, String idx)
	{
		this.asmFile.println("@SP");
		this.asmFile.println("M=M-1");
		this.asmFile.println("A=M");
		this.asmFile.println("D=M");
		
		this.asmFile.println("@R13");
		this.asmFile.println("M=D");
		
		if (basePtr.equals(STAT))
		{
			this.asmFile.println("@"+this.fileName+"."+idx);
			this.asmFile.println("D=A");

		}
		
		else
		{
		
			this.asmFile.println("@" + basePtr);
			
			if (basePtr.equals(TMP))
				this.asmFile.println("D=A");
			else
				this.asmFile.println("D=M");
			this.asmFile.println("@" + idx);
			this.asmFile.println("D=A+D");
		}
		
		this.asmFile.println("@R13");
		this.asmFile.println("D=D+M");
		this.asmFile.println("A=D-M");
		this.asmFile.println("M=D-A");
	}
	
	/*
	 * Pop the value from stack and set it in the register.
	 */
	public void pushToStack(String register)
	{
		this.asmFile.println(register);
		this.asmFile.println("D=M");
		
		this.asmFile.println("@SP");
		this.asmFile.println("A=M");
		this.asmFile.println("M=D");
		
		this.asmFile.println("@SP");
		this.asmFile.println("M=M+1");
	}
	
	/*
	 * Pop the value from stack and set it in the register.
	 */
	public void pushToStack(String basePtr, String idx)
	{
		if (basePtr.equals(STAT))
		{
			this.asmFile.println("@" +this.fileName+"."+idx);
		}else{
			this.asmFile.println("@" + basePtr);
			if (basePtr.equals(TMP))
				this.asmFile.println("D=A");
			else
				this.asmFile.println("D=M");
			this.asmFile.println("@" + idx);
			this.asmFile.println("A=A+D");
		}
		this.asmFile.println("D=M");
		
		this.asmFile.println("@SP");
		this.asmFile.println("A=M");
		this.asmFile.println("M=D");
		
		this.asmFile.println("@SP");
		this.asmFile.println("M=M+1");
	}
	
	/*
	 * Pop the value from stack and set it in the register.
	 */
	private void pushConstantToStack(String constant)
	{
		
		this.asmFile.println("@"+constant);
		this.asmFile.println("D=A");
		
		this.asmFile.println("@SP");
		this.asmFile.println("A=M");
		this.asmFile.println("M=D");
		
		this.asmFile.println("@SP");
		this.asmFile.println("M=M+1");
	}
	
	private void setTrueCondition()
	{
		this.asmFile.println("(TRUE_COND_"+ countCond+ ")");
		this.asmFile.println("@R13");
		this.asmFile.println("M=-1");	
	}
	
	private void setFalseCondition()
	{
		this.asmFile.println("@R13");
		this.asmFile.println("M=0");	
		this.asmFile.println("@END_CONDITION_"+ Integer.toString(countCond));
		this.asmFile.println("0;JMP");
	}
	
	private void isNegative()
	{
		this.asmFile.println("@R13");
		this.asmFile.println("D=M");
		this.asmFile.println("@COND_OVERFLOW_NEGATIVE" + countCond);
		this.asmFile.println("D;JLT");
		falseOverFlowNegative();
		isPositiveNegative();
		falseOverFlowNegative();
		trueOverFlowNegative();
		
	}
	
	
	private void isPositiveNegative()
	{
	
		this.asmFile.println("(COND_OVERFLOW_NEGATIVE" + countCond +")");
		this.asmFile.println("@R14");
		this.asmFile.println("D=M");
		this.asmFile.println("@SEC_COND_OVERFLOW_NEGATIVE" + countCond);
		this.asmFile.println("D;JGT");
	}
	
	private void falseOverFlowNegative()
	{
		this.asmFile.println("@START_COND"+ Integer.toString(countCond));
		this.asmFile.println("0;JMP");
	}
	
	
	
	private void trueOverFlowNegative()
	{
		this.asmFile.println("(SEC_COND_OVERFLOW_NEGATIVE" + countCond +")");
		this.asmFile.println("@R13");
		this.asmFile.println("M=0");
		this.asmFile.println("@END_CONDITION_"+ Integer.toString(countCond));
	}
	
	
	private void falseOverFlow()
	{
		this.asmFile.println("@START_COND"+ Integer.toString(countCond));
		this.asmFile.println("0;JMP");
	}
	
	
	
	private void trueOverFlow()
	{
		this.asmFile.println("(SEC_COND_OVERFLOW" + countCond +")");
		this.asmFile.println("@R13");
		this.asmFile.println("M=-1");
		this.asmFile.println("@END_CONDITION_"+ Integer.toString(countCond));
	}
	
	
	private void isPositive()
	{
	
		this.asmFile.println("(COND_OVERFLOW" + countCond +")");
		this.asmFile.println("@R14");
		this.asmFile.println("D=M");
		this.asmFile.println("@SEC_COND_OVERFLOW" + countCond);
		this.asmFile.println("D;JLT");
	}

	private void checkOverFlow()
	{
		this.countCond++;
		this.asmFile.println("@R13");
		this.asmFile.println("D=M");
		this.asmFile.println("@COND_OVERFLOW" + countCond);
		this.asmFile.println("D;JGT");
		isNegative();
		isPositive();
		falseOverFlow();
		trueOverFlow();
	}
	
	/*
	 * Write arithmetic operation.
	 */
	public void writeArithmetic(String command)
	{
		popFromStack("@R14");
		this.asmFile.println("@R14");
		this.asmFile.println("D=M");
		this.asmFile.println("@R15");
		
		if (command.equals("neg"))
		{
			this.asmFile.println("M=-D");
			pushToStack("@R15");
			return;
		}
		
		if (command.equals("not"))
		{
			this.asmFile.println("M=!D");
			pushToStack("@R15");
			return;
		}
		
		popFromStack("@R13");
		this.asmFile.println("@R14");
		this.asmFile.println("D=M");
		this.asmFile.println("@R13");
		
		if (command.equals("sub"))
			this.asmFile.println("M=M-D");
		
		else if (command.equals("add"))
			this.asmFile.println("M=M+D");
		
		else if (command.equals("or"))
			this.asmFile.println("M=M|D");
		
		else if (command.equals("and"))
			this.asmFile.println("M=M&D");
		
		else
		{
			checkOverFlow();
			this.asmFile.println("(START_COND"+ Integer.toString(countCond)+ ")");
			this.asmFile.println("@R14");
			this.asmFile.println("D=M");
			this.asmFile.println("@R13");
			this.countCond++;
			this.asmFile.println("M=M-D");
			this.asmFile.println("D=M");
			this.asmFile.println("@TRUE_COND_" + countCond);
			if (command.equals("eq"))
				this.asmFile.println("D;JEQ");
			
			else if (command.equals("lt"))
				this.asmFile.println("D;JLT");
			
			else
				this.asmFile.println("D;JGT");
			
			setFalseCondition();
			setTrueCondition();
			this.asmFile.println("(END_CONDITION_"+ Integer.toString(countCond)+ ")");
		}
		pushToStack("@R13");
	}
	


	/**
	 * Push or pop to the legal segment.
	 * @param command - push or pop
	 * @param segment - the segment
	 * @param index - the index in the segment
	 */
	public void writePushPop(CommandType command, String segment, String index)
	{
		if (command == CommandType.C_PUSH)
		{
			if (segment.equals("constant"))
				pushConstantToStack(index);
			
			else if (segment.equals("local"))
				pushToStack("LCL", index);
			
			else if (segment.equals("static"))
				pushToStack(STAT, index);
				
			else if (segment.equals("this"))
				pushToStack("THIS", index);
			
			else if (segment.equals("that"))
				pushToStack("THAT", index);
			
			else if (segment.equals("pointer"))
			{
				if (index.equals("0"))
					pushToStack("@THIS");
				else
					pushToStack("@THAT");
			}
			
			else if (segment.equals("temp"))
				pushToStack(TMP, index);
			
			else if (segment.equals("argument"))
				pushToStack("ARG", index);
			
			else
				System.out.println("ERROR COMMAND"); 
		}
		
		else
		{
			if (segment.equals("constant"))
				popFromStack(index);
			
			else if (segment.equals("local"))
				popFromStack("LCL", index);
			
			else if (segment.equals("static"))
				popFromStack(STAT, index);
				
			else if (segment.equals("this"))
				popFromStack("THIS", index);
			
			else if (segment.equals("that"))
				popFromStack("THAT", index);
			
			else if (segment.equals("pointer"))
			{
				if (index.equals("0"))
					popFromStack("@THIS");
				else
					popFromStack("@THAT");
			}
			
			else if (segment.equals("temp"))
				popFromStack(TMP, index);
			
			else if (segment.equals("argument"))
				popFromStack("ARG", index);
			
			else
				System.out.println("ERROR COMMAND"); 	
		}
		
	}
	
	public void close()
	{
		this.asmFile.close();
	}
	
	
}
