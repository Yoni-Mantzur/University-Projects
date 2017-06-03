
/**
 * Class of finals and regexes
 * @author Yoni
 *
 */
public abstract class Regexes 
{
	// C_ARITMETHIC
	public static final String C_ARITMETHIC = "(add|sub|neg|eq|gt|lt|and|or|not)";
	
	// The number of the group:
	public static final int ARITHMETIC_OPER = 1;
	
	private static final String segments = "(argument|local|static|constant|this|that|pointer|temp)";
	
	// C_push_pop 
	public static final String C_PUSH = "(push)" + segments + "(\\d+)";
	public static final String C_POP = "(pop)" + segments + "(\\d+)";
	
	// C_LABEL_GOTO_IF
	public static final String C_LABEL = "(label)(.+)";
	public static final String C_GOTO = "(goto)(.+)";
	public static final String C_IF = "(if-goto)(.+)";
	
	
	// C_FUNCTION_CALL
	public static final String C_FUNCTION = "(\\s*function)(.+)(\\s+\\d+\\s*)";
	public static final String C_CALL = "(\\s*call)(.+)(\\s+\\d+\\s*)";
	
	
	
	// C_RETURN
	public static final String C_RETURN = "(return)";
	

	// Groups of ARGUMENTS
	public static final int COMMAND_NAME = 1;
	public static final int ARG1 = 2;
	public static final int ARG2 = 3;


	public static final String COMMENT = "//*";
	
}


