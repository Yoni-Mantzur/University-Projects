
/**
 * Translates asm code to binary code.
 * @author Yoni
 *
 */
public abstract class Code 
{
	private static final String A_REG = "A", M_REG = "M", D_REG = "D";
	
	/**
	 * @param destASM - the dest value in asmbly.
	 * @return the dest value in binary
	 */
	public static String dest(String destASM)
	{
		int destB = 0b000;
		
		if (destASM == null)
			return Integer.toBinaryString(destB);
		
		if (destASM.contains(A_REG))
			destB += 0b100;
		
		if (destASM.contains(D_REG))
			destB += 0b010;
		
		if (destASM.contains(M_REG))
			destB += 0b001;
		
		return Integer.toBinaryString(destB);
	}
	
	/**
	 * @param compASM - the comp value in asmbly.
	 * @return the comp value in binary
	 */
	public static String comp(String compASM)
	{
		int compB = 0b0000000;
		
		if (compASM.contains(M_REG))
			compB += 0b1000000;
			
		if (compASM.equals("0"))
			compB += 0b101010;
		
		else if (compASM.equals("1"))
			compB += 0b111111;
		
		else if (compASM.equals("-1"))
			compB += 0b111010;
		
		else if (compASM.equals(D_REG))
			compB += 0b001100;
				
		else if (compASM.equals(A_REG) || compASM.equals(M_REG))
			compB += 0b110000;
		
		else if (compASM.equals("!"+D_REG))
			compB += 0b001101;
		
		else if (compASM.equals("!"+A_REG) || compASM.equals("!"+M_REG))
			compB += 0b110001;
		
		else if (compASM.equals("-"+D_REG))
			compB += 0b001111;
		
		else if (compASM.equals("-"+A_REG) || compASM.equals("-"+M_REG))
			compB += 0b111010;
		
		else if (compASM.equals(D_REG+"+1"))
			compB += 0b011111;
		
		else if (compASM.equals(A_REG+"+1") || compASM.equals(M_REG+"+1"))
			compB += 0b110111;
		
		else if (compASM.equals(D_REG+"-1"))
			compB += 0b001110;
		
		else if (compASM.equals(A_REG+"-1") || compASM.equals(M_REG+"-1"))
			compB += 0b110010;
		
		else if (compASM.equals(D_REG+"+"+A_REG) || compASM.equals(D_REG+"+"+M_REG))
			compB += 0b000010;
		
		else if (compASM.equals(D_REG+"-"+A_REG) || compASM.equals(D_REG+"-"+M_REG))
			compB += 0b010011;
		
		else if (compASM.equals(A_REG+"-"+D_REG) || compASM.equals(M_REG+"-"+D_REG))
			compB += 0b000111;
		
		else if (compASM.equals(D_REG+"&"+A_REG) || compASM.equals(D_REG+"&"+M_REG))
			compB += 0b000000;
		
		else if (compASM.equals(D_REG+"|"+A_REG) || compASM.equals(D_REG+"|"+M_REG))
			compB += 0b010101;
		
		else if (compASM.equals("M>>"))
			compB += 0b000000;
		
		else if (compASM.equals("A>>"))
			compB += 0b000000;
		
		else if (compASM.equals("D>>"))
			compB += 0b010000;
		
		else if (compASM.equals("M<<"))
			compB += 0b100000;
		
		else if (compASM.equals("A<<"))
			compB += 0b100000;
		
		else if (compASM.equals("D<<"))
			compB += 0b110000;

		else
		{
			System.err.println("INVALID COMP");
			System.exit(1);
		}
		
		return Integer.toBinaryString(compB);
	}
	
	/**
	 * @param jmpASM - the jmp value in asmbly.
	 * @return the jmp value in binary
	 */
	public static String jmp(String jmpASM)
	{
		int jmpB = 0b000;
		
		if (jmpASM == null)
		{
			return Integer.toBinaryString(jmpB);
		}
		
		if (jmpASM.equals("JGT"))
			jmpB = 0b001;
		
		else if (jmpASM.equals("JEQ"))
			jmpB = 0b010;

		else if (jmpASM.equals("JGE"))
			jmpB = 0b011;
		
		else if (jmpASM.equals("JLT"))
			jmpB = 0b100;
		
		else if (jmpASM.equals("JNE"))
			jmpB = 0b101;
		
		else if (jmpASM.equals("JLE"))
			jmpB = 0b110;
		
		else if (jmpASM.equals("JMP"))
			jmpB = 0b111;
		
		else
		{
			System.err.println("INVALID JMP");
			System.exit(1);
		}
		
		return Integer.toBinaryString(jmpB);
	}
	
}