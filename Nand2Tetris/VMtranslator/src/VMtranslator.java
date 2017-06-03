import java.io.File;

public class VMtranslator 
{

	/**
	 * Program that translates .vm files to asm files
	 * @param args - the directory or file path to vm files.
	 */
	public static void main(String[] args) 
	{

		File fileName = new File(args[0]);		
		File files[] = fileName.listFiles();
		
		
		int index = fileName.getPath().lastIndexOf("vm");
		String newPath;
		if (index == -1)
			newPath = fileName.getPath() + File.separator + fileName.getName() + ".asm";
	
		else
			newPath = fileName.getPath().substring(0, index) + "asm";
		
		CodeWriter asmFile = new CodeWriter(newPath);
		
		if (files == null)
		{
			files = new File[1];
			files[0] = fileName;
		}
		
		
		
		for (int i = 0; i < files.length; i++)
		{
			if (!files[i].isDirectory())
			{
			
				String path = files[i].getPath();
				int idxEnd = path.lastIndexOf("vm");
				if (idxEnd == -1)
					continue;
				
				int idxStart = path.lastIndexOf(File.separator);
				if (idxStart == -1)
					asmFile.setFileName(path);
				else
					asmFile.setFileName(path.substring(idxStart+1, idxEnd-1));
				
				Parser parser = new Parser(path);
				
				CommandType typeLine;
				do
				{			
					parser.advanceLine();
					typeLine = parser.commandType();
					
					if (typeLine == CommandType.C_PUSH || typeLine == CommandType.C_POP)
						asmFile.writePushPop(typeLine, parser.arg1(), parser.arg2());
						
					
					else if (typeLine == CommandType.C_ARITMETHIC)
						asmFile.writeArithmetic(parser.arg0());
					
					else if (typeLine == CommandType.C_LABEL)
						asmFile.writeLabel(parser.arg1());
					
					else if (typeLine == CommandType.C_GOTO)
						asmFile.writeGoTo(parser.arg1());
					
					else if (typeLine == CommandType.C_IF)
						asmFile.writeIfGoTo(parser.arg1());
					
					else if (typeLine == CommandType.C_FUNCTION)
						asmFile.writeFunction(parser.arg1(), parser.arg2());

					else if (typeLine == CommandType.C_CALL)
						asmFile.writeCall(parser.arg1(), parser.arg2());
					
					else if (typeLine == CommandType.C_RETURN)
						asmFile.writeReturn();
			
					
					else
						continue;
			
				}while (!parser.isEndFile());
			}
		}
		
		asmFile.close();
		
		
		
		
//		Pattern p = Pattern.compile(Regexes.C_RETURN);
//		Matcher m = p.matcher("return");
//		
//		System.out.println(m.matches());
//		
//		for (int i =0; i<=m.groupCount(); i++)
//			System.out.println(m.group(i));
//		
//		String ff = "hello//sdkjks";
//		System.out.println(ff.replaceFirst("//.*", ""));
	}

}
