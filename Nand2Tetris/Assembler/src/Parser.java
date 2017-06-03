import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Parser class of asm files
 * @author Yoni
 *
 */
public class Parser 
{
	
	// The file to read from
	private BufferedReader assemblyFile;
	
	// The lines currently reading
	private String currentLine, nextLine;
	
	private static final String SPACE_CHAR = "\\s";
	
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
			this.assemblyFile = new BufferedReader(new FileReader(filePath));
			this.currentLine = null;
			this.nextLine = this.assemblyFile.readLine();
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
			this.nextLine = this.assemblyFile.readLine();
		
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
	
	/**
	 * @return the type of the command in the current line
	 */
	public CommandType commandType()
	{ 
		this.currentTypeCommand = CommandType.NON_COMMAND;
		
		this.currentLine = this.currentLine.replaceAll(SPACE_CHAR, "");
				
		// Check the type of the command
		if (checkRegex(Regexes.A_COMMAND_LINE, this.currentLine))
			this.currentTypeCommand = CommandType.A_COMMAND;
		
		else if (checkRegex(Regexes.C_COMMAND_LINE, this.currentLine))
			this.currentTypeCommand =  CommandType.C_COMMAND;
		
		else if (checkRegex(Regexes.LABEL_COMMAND_LINE, this.currentLine))
			this.currentTypeCommand =  CommandType.LABEL_COMMAND;
		
		else if (checkRegex(Regexes.SHIFT_COMMAND, this.currentLine))
			this.currentTypeCommand =  CommandType.SHIFT_COMMAND;
		
		return this.currentTypeCommand;
	}
	
	/**
	 * @return the symbol of the A-command
	 * @exception - if current line isn't A-command, exit.
	 */
	public String symbol()
	{
		if (currentTypeCommand != CommandType.A_COMMAND && 
						currentTypeCommand != CommandType.LABEL_COMMAND)
		{
			System.err.println("IS'NT LEGAL TYPE COMMAND");
			System.exit(1);	
		}
		
		String symbol = this.matcher.group(Regexes.SYMBOL);
		
		if (currentTypeCommand == CommandType.A_COMMAND && symbol.contains("//"))
		{
			symbol.replace("//.*", "");
		}
			
		return symbol;
	}
	
	/**
	 * @return the dest of the C-command
	 * @exception - if current line isn't C-command, exit.
	 */
	public String dest()
	{
		if (currentTypeCommand != CommandType.C_COMMAND && currentTypeCommand != CommandType.SHIFT_COMMAND)
		{
			System.err.println("IS'NT LEGAL TYPE COMMAND");
			System.exit(1);	
		}
		return this.matcher.group(Regexes.DEST);
	}
	
	/**
	 * @return the comp of the C-command
	 * @exception - if current line isn't C-command, exit.
	 */
	public String comp()
	{
		if (currentTypeCommand != CommandType.C_COMMAND && currentTypeCommand != CommandType.SHIFT_COMMAND)
		{
			System.err.println("IS'NT LEGAL TYPE COMMAND");
			System.exit(1);	
		}
		return this.matcher.group(Regexes.COMP);
	}
	
	/**
	 * @return the jmp of the C-command
	 * @exception - if current line isn't C-command, exit.
	 */
	public String jmp()
	{
		if (currentTypeCommand != CommandType.C_COMMAND && currentTypeCommand != CommandType.SHIFT_COMMAND)
		{
			System.err.println("IS'NT LEGAL TYPE COMMAND");
			System.exit(1);	
		}
		return this.matcher.group(Regexes.JMP);
	}
	


}
