
/**
 * Class of finals and regexes
 * @author Yoni
 *
 */
public abstract class Regexes 
{
	// C-COMMAND
	public static final String C_COMMAND_LINE = "(?:(A?M?D?)(?:=))?([AMD01-1]|[-!][AMD1]|"
												+ "[AMD][+-][AMD1]|[AMD][&|][AMD]);?"
												+ "(JMP|JLE|JNE|JLT|JGE|JEQ|JGT)?(//.*)?";
	// The number of the group:
	public static final int DEST = 1;
	public static final int COMP = 2;
	public static final int JMP = 3;
	
			
	// A-COMMAND
	public static final String A_COMMAND_LINE = "@(.*)";
		
	// LABEL-COMMAND
	public static final String LABEL_COMMAND_LINE = "[(](.*)[)](//.*)?";
	
	//SHIFT COMMAND
	public static final String SHIFT_COMMAND = "(?:(A?M?D?)(?:=))?([AMD]<<|[AMD]>>);?"
											   + "(JMP|JLE|JNE|JLT|JGE|JEQ|JGT)?(//.*)?";
	
	// The number of the group:
	public static final int SYMBOL = 1;

}

