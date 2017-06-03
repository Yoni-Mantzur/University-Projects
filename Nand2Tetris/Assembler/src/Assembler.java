import java.io.File;
import java.io.PrintWriter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * The program get asm file and output the hack file.
 * @author Yoni
 *
 */
public class Assembler 
{
	private static final int LENGTH_ADD_BIT = 15, LEN_DES_BITS = 3, 
							 LEN_COMP_BITS = 7, LEN_JMP_BITS = 3;
	
	private static int freeAddress = 16;
	
	private static String paddingBin(String binaryNum, int numBits)
	{
		int reminder = numBits - binaryNum.length();
		
		for (int i = 0; i < reminder; i++)
			binaryNum = "0" + binaryNum;
		
		return binaryNum;
	}
	
	private static int getAddress(String symbol, SymbolTable table)
	{
		if (table.isContains(symbol))
			return table.getAddress(symbol);
	 
		table.addEntry(symbol, freeAddress);
		freeAddress++;
		return freeAddress-1;		
	}
	
	private static String aCommand(Parser parser, SymbolTable table)
	{
		String symbolStr = parser.symbol();
		int symbol;
		
		if (symbolStr.matches("\\d+"))
			symbol = Integer.parseInt(symbolStr);
		else
			symbol = getAddress(symbolStr, table);
		
		return paddingBin(Integer.toBinaryString(symbol), LENGTH_ADD_BIT);
	}
	
	private static String cCommand(Parser parser)
	{
		String destBin = paddingBin(Code.dest(parser.dest()), LEN_DES_BITS),
			   compBin = paddingBin(Code.comp(parser.comp()), LEN_COMP_BITS),
			   jmpBin  = paddingBin(Code.jmp(parser.jmp()), LEN_JMP_BITS);
		

		return compBin + destBin + jmpBin;
	}
	
	
	private static void loadKnownSymbols(SymbolTable table)
	{
		// Adding predefined entries.
		
		for (int i = 0; i <= 15; i++)
		{
			table.addEntry("R"+ Integer.toString(i), i);
		}
		
		table.addEntry("SCREEN", 16384);
		table.addEntry("KBD", 24576);
		table.addEntry("SP", 0);
		table.addEntry("LCL", 1);
		table.addEntry("ARG", 2);
		table.addEntry("THIS", 3);
		table.addEntry("THAT", 4);
		
	}
	
	private static void addLabels(SymbolTable table, String filePath)
	{
		int counterLines = 0;
		Parser parser = new Parser(filePath);
		CommandType typeLine;
		String symbol;
		
		do
		{
			parser.advanceLine();
			typeLine = parser.commandType();
			
			if (typeLine == CommandType.LABEL_COMMAND)
			{
				symbol = parser.symbol();
				
				if (!table.isContains(symbol))
					table.addEntry(symbol, counterLines);
			}
			
			else if (typeLine != CommandType.NON_COMMAND)
				counterLines++;
			
		}while(!parser.isEndFile());
		
	}
	
	private static SymbolTable initSymbolTable(String filePath)
	{
		freeAddress = 16;
		SymbolTable table = new SymbolTable();
		
		// Initialize known symbols
		loadKnownSymbols(table);
		
		// Initialize labels
		addLabels(table, filePath);
		
		return table;
	}

	public static void main(String[] args)  throws Exception
	{
//		File fileName = new File(args[0]);		
//		File files[] = fileName.listFiles();
//		
//		if (files == null)
//		{
//			files = new File[1];
//			files[0] = fileName;
//		}
//		
//		for (int i = 0; i < files.length; i++)
//		{
//			if (!files[i].isDirectory())
//			{
//				String path = files[i].getPath();
//					
//				SymbolTable table = initSymbolTable(path);
//				
//				Parser parser = new Parser(path);
//				int index = path.lastIndexOf("asm");
//				String newPath = path.substring(0, index) + "hack";
//				PrintWriter hackFile = new PrintWriter(newPath);
//				String lineBin = "";
//				CommandType typeLine;
//				
//				do
//				{			
//					parser.advanceLine();
//					lineBin = "";
//					typeLine = parser.commandType();
//					
//					if (typeLine == CommandType.A_COMMAND)
//						lineBin = "0" + aCommand(parser, table);
//					
//					else if (typeLine == CommandType.C_COMMAND)
//						lineBin = "111" + cCommand(parser);
//		
//					else if (typeLine == CommandType.SHIFT_COMMAND)
//						lineBin = "101" + cCommand(parser);
//					
//					else
//						continue;
//					
//					hackFile.println(lineBin);
//			
//				}while (!parser.isEndFile());
//				hackFile.close();
//			}
//		}
		
		
//		
		String a = "function 	sys.dd 22";
		Pattern p = Pattern.compile("^\\s*(function|call).*");
		Matcher matcher = p.matcher(a);
		System.out.println(matcher.matches());
		System.out.println(matcher.group());

		
		
		
	}

}
