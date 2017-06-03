import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Class charge of parser vm file.
 * @author Yoni
 *
 */
public class Parser 
{
	// The file to read from
	private BufferedReader vmFile;

	// The lines currently reading
	private String currentLine, nextLine;
	
	// Charge of what type of current line is
	private CommandType currentTypeCommand;
	
	// Regex tools
	private Pattern pattern;
	private Matcher matcher;
	
	/**
	 * Constructor.
	 * @param filePath - the path of source file
	 * @throws IOException - loading file failed
	 */
	public Parser(String filePath)
	{
		try
		{
			this.vmFile = new BufferedReader(new FileReader(filePath));
			this.nextLine = this.vmFile.readLine();
			this.currentLine = null;
			this.currentTypeCommand = CommandType.NON_COMMAND;
			
		}catch(IOException e)
		{
			System.err.println(e.getMessage());
		}
	}
	
	/**
	 * @return true if end of file 
	 */
	public boolean isEndFile()
	{
		if (this.nextLine == null)
			return true;
		
		return false; 
	}
	
	/**
	 * Read the next line.
	 */
	public void advanceLine() 
	{
		try
		{
			this.currentLine = this.nextLine;
			removeComments();
			this.nextLine = this.vmFile.readLine();
		
		}catch(IOException e)
		{
			System.err.println("Error IO");
		}
	}
	
	/*
	 * Checks the given regex on the given metcher.
	 */
	private boolean checkRegex(String regex, String matcher)
	{
		this.pattern = Pattern.compile(regex);
		this.matcher = pattern.matcher(matcher);
		
		return this.matcher.matches();
	}
	
	/*
	 * Remove comments from the current line.
	 */
	private void removeComments()
	{
		this.currentLine = this.currentLine.replaceAll("\n", "");
		this.currentLine = this.currentLine.replaceFirst("//.*", "");
	}
	
	
	private boolean checkFunctionCall()
	{
		Pattern p = Pattern.compile("^\\s*(function|call).*");
		Matcher matcher = p.matcher(this.currentLine);
		return matcher.matches();
	}
	
	/**
	 * @return the type of the command in the current line
	 */
	public CommandType commandType()
	{ 
		this.currentTypeCommand = CommandType.NON_COMMAND;
		
		if (checkRegex(Regexes.COMMENT, this.currentLine) || this.currentLine.equals("")
				|| this.currentLine == null)
			return this.currentTypeCommand;
		
		if (checkFunctionCall())
		{
			if (checkRegex(Regexes.C_CALL, this.currentLine))
				this.currentTypeCommand = CommandType.C_CALL;
			
			else if (checkRegex(Regexes.C_FUNCTION, this.currentLine))
				this.currentTypeCommand = CommandType.C_FUNCTION;
		}else{
			 
		this.currentLine = this.currentLine.replaceAll("\\s", "");
		// Check the type of the command
		if (checkRegex(Regexes.C_ARITMETHIC, this.currentLine))
			this.currentTypeCommand = CommandType.C_ARITMETHIC;
		
		else if (checkRegex(Regexes.C_POP, this.currentLine))
			this.currentTypeCommand =  CommandType.C_POP;
		
		else if (checkRegex(Regexes.C_PUSH, this.currentLine))
			this.currentTypeCommand =  CommandType.C_PUSH;
		
		else if (checkRegex(Regexes.C_LABEL, this.currentLine))
			this.currentTypeCommand =  CommandType.C_LABEL;

		else if (checkRegex(Regexes.C_GOTO, this.currentLine))
			this.currentTypeCommand =  CommandType.C_GOTO;
		
		else if (checkRegex(Regexes.C_IF, this.currentLine))
			this.currentTypeCommand =  CommandType.C_IF;

		else if (checkRegex(Regexes.C_FUNCTION, this.currentLine))
			this.currentTypeCommand =  CommandType.C_FUNCTION;
		
		else if (checkRegex(Regexes.C_RETURN, this.currentLine))
			this.currentTypeCommand = CommandType.C_RETURN;
		}
		
		return this.currentTypeCommand;
	}
	
	/**
	 * @return the name of the command
	 */
	public String arg0()
	{	
		return this.matcher.group(Regexes.COMMAND_NAME).trim();
	}
	
	/**
	 * @return the first argument of the command
	 * @exception - if current line isn't command or return command, exit.
	 */
	public String arg1()
	{
		if (currentTypeCommand == CommandType.NON_COMMAND ||
						currentTypeCommand == CommandType.C_RETURN)
		{
			System.err.println("IS'NT LEGAL TYPE COMMAND");
			System.exit(1);	
		}
		
		return this.matcher.group(Regexes.ARG1).trim();
	}
	
	/**
	 * @return the second argument of the command
	 * @exception - if current line isn't command or return command, exit.
	 */
	public String arg2()
	{
		if (currentTypeCommand != CommandType.C_POP && currentTypeCommand != CommandType.C_PUSH && 
						currentTypeCommand != CommandType.C_FUNCTION && 
						currentTypeCommand != CommandType.C_CALL )
		{
			System.err.println("IS'NT LEGAL TYPE COMMAND");
			System.exit(1);	
		}
		
		return this.matcher.group(Regexes.ARG2).trim();
	}
}
