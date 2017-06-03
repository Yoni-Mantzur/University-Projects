import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;


/**
 * Class charge of parser jack file.
 * @author Yoni
 *
 */
public class Parser 
{
	// The file to read from
	private BufferedReader jackFile;

	// The lines currently reading
	private String currentLine, nextLine;
	
	private String[] listLine;
	
	private int numWord;
	
	int currentString;
	private ArrayList<String> listStrings;

	
	
	/**
	 * Constructor.
	 * @param filePath - the path of source file
	 * @throws IOException - loading file failed
	 */
	public Parser(String jackFile)
	{
		try{
			listStrings = new ArrayList<>();
			getAllString(jackFile);
			this.jackFile = new BufferedReader(new FileReader(jackFile));
			this.nextLine = this.jackFile.readLine();
		}catch(IOException e){
			System.err.println("Error Contructing Parser object");
		}
		this.currentLine = null;
		this.numWord = 0; 
		this.currentString = 0;
		this.listLine = null;
	}
	
	private String checkCommentsInLine(String currentLine, BufferedReader reader, boolean oper) throws IOException
	{
		if (currentLine == null)
			return currentLine;
		// Cut comments
		
		if (oper)
		{	
			int ind = currentLine.lastIndexOf("\"");
			int ind1 = currentLine.indexOf("\"");
			int ind2 = currentLine.indexOf("//");
			int ind3 = currentLine.indexOf("//*");
			int ind4 = currentLine.indexOf("/*");
			int ind5 = currentLine.indexOf("*/");
			if (ind3 < ind1 && (ind5 < ind1 && ind5 != -1) || (ind3 > ind && (ind5 > ind && ind5 != -1))){
				currentLine = currentLine.replaceAll("/\\*\\*(.*)\\*/", " ");
			}
			if ((ind4 < ind1 && (ind5 < ind1 && ind5 != -1)) || (ind4 > ind && (ind5 > ind && ind5 != -1))){
				currentLine = currentLine.replaceAll("/\\*\\*(.*)\\*/", " ");
			}
			if (ind2 < ind1 || (ind2 > ind && ind1 != -1)){
				// Replace all row comments with one space
				currentLine = currentLine.replaceAll("//.*", "");
			}
			
			if (ind < ind2 || ind < ind3 || ind < ind4)
				return currentLine;
		}
		
		else
		{
			currentLine = currentLine.replaceAll("\"(.*?)\"", " \" \" ");
			currentLine = currentLine.replaceAll("(/\\*(.*?)\\*/)", " ");
			currentLine = currentLine.replaceAll("/\\*\\*(.*?)\\*/", " ");
			currentLine = currentLine.replaceAll("//.*", "");
		}
		
		int idx;
		if (((idx = currentLine.indexOf("/*")) != -1 || (idx = currentLine.indexOf("/**"))!= -1) && currentLine.indexOf("*/") == -1)
		{
			if (idx > 0)
				currentLine = currentLine.substring(0, idx);
			else
				currentLine = "";
			
			String newLine = reader.readLine();
			int newIdx = -2;
			while(newLine != null && (newIdx = newLine.indexOf("*/")) == -1)
			{
				newLine = reader.readLine();
			}
			
			
			if (newLine != null)
				return currentLine += newLine.substring(newIdx+2);
		}
		return currentLine;
		
	}
	
	
	private void getAllString(String jackFile) throws IOException
	{
		BufferedReader reader = new BufferedReader(new FileReader(jackFile));
		
		String curLine = reader.readLine(), str="";
		curLine = checkCommentsInLine(curLine, reader, true);
		int indexStartStr, indexEndStr;
		while (curLine != null)
		{
			while ((indexStartStr = curLine.indexOf("\"")) != -1)
			{
				int oldLineSize = curLine.length();
				curLine = curLine.substring(indexStartStr+1);
						
				indexStartStr -= (oldLineSize - curLine.length()-1);
				while ((indexEndStr = curLine.indexOf("\"")) == -1 && curLine != null)
				{
					indexStartStr = 0;
					str += curLine;
					curLine = reader.readLine();
					curLine = checkCommentsInLine(curLine, reader, true);
				}
				str += curLine.substring(indexStartStr, indexEndStr);
				str = str.replaceAll("\t", "\\\\t");
				str = str.replaceAll("\n", "\\\\n");
				listStrings.add(str);
				curLine = curLine.substring(indexEndStr+1);
				str = "";
			}
			curLine = reader.readLine();
			curLine = checkCommentsInLine(curLine, reader,true);
		}
		reader.close();
	}
	
	/**
	 * @return true if end of file 
	 */
	private boolean isEndFile()
	{
		return this.nextLine == null;
	}
	
	/**
	 * Read the next line.
	 */
	private void advanceLine() 
	{
		try
		{
			this.currentLine = this.nextLine;
			
			this.currentLine = checkCommentsInLine(this.currentLine, this.jackFile, false);
			removeComments();
						
			this.listLine = creatListLine();
			this.numWord = 0;
			
			this.nextLine = this.jackFile.readLine();
			
		
		}catch(IOException e)
		{
			System.err.println("Error Reading from jack File after line: " + this.currentLine);
		}
	}
	
	
	private void replaceSymbolsWithSpace()
	{
		this.currentLine = this.currentLine.replaceAll("\\{", " \\{ ");
		this.currentLine = this.currentLine.replaceAll("}", " \\} ");
		this.currentLine = this.currentLine.replaceAll("\\(", " \\( ");
		this.currentLine = this.currentLine.replaceAll("\\)", " \\) ");
		
		this.currentLine = this.currentLine.replaceAll("\\[", " \\[ ");
		this.currentLine = this.currentLine.replaceAll("]", " \\] ");
		this.currentLine = this.currentLine.replaceAll("\\.", " \\. ");
		this.currentLine = this.currentLine.replaceAll("\\,", " \\, ");
		
		this.currentLine = this.currentLine.replaceAll("\\;", " \\; ");
		this.currentLine = this.currentLine.replaceAll("\\+", " \\+ ");
		this.currentLine = this.currentLine.replaceAll("\\-", " \\- ");
		this.currentLine = this.currentLine.replaceAll("\\*", " \\* ");
		
		this.currentLine = this.currentLine.replaceAll("\\/", " \\/ ");
		this.currentLine = this.currentLine.replaceAll("\\&", " \\& ");
		this.currentLine = this.currentLine.replaceAll("\\|", " \\| ");
		this.currentLine = this.currentLine.replaceAll("\\<", " \\< ");
		
		this.currentLine = this.currentLine.replaceAll("\\>", " \\> ");
		this.currentLine = this.currentLine.replaceAll("\\=", " \\= ");
		this.currentLine = this.currentLine.replaceAll("\\~", " \\~ ");
		this.currentLine = this.currentLine.replaceAll("\"", " \" ");
	}
	
	/*
	 * Remove comments from the current line.
	 */
	private void removeComments()
	{
		// Replace several spaces with one space
		this.currentLine = this.currentLine.replaceAll("\\s+", " ");
		replaceSymbolsWithSpace();	
	}
	
	
	private String[] creatListLine()
	{
		return this.currentLine.split(" ");
	}
	
	private String getCurrentValue(){
		String value = listLine[numWord];
		numWord++;
		
		return value;
	}
	
	
	public String getFirstToken()
	{
		advanceLine();
		return getValueToken();
	}
	
	private boolean setNumWordLegal()
	{
		while (numWord >= listLine.length)
		{
			if (isEndFile())
				return false;
			advanceLine();
		}
		return true;
	}
	

	private void moveToNextLegalWord()
	{
		while(!listLine[numWord].equals("\""))
		{
			numWord++;
			if (!setNumWordLegal()) // Never get inside for legal input
				return;
		}
		
		numWord++;
	}
		
		
	
	public String getValueToken()
	{
		// Means no more to read
		if (!setNumWordLegal())
			return null;
		
		String currentWord = listLine[numWord];
		
		if (currentWord.matches("\\s+") || currentWord.equals(""))
		{
			numWord++;
			return getValueToken();
		}
		
		else if (currentWord.equals("\""))
		{    
			numWord++;
			moveToNextLegalWord();
			currentString++;
			return "@"+listStrings.get(currentString-1);
		}
		
		
		return getCurrentValue();
	}

}
