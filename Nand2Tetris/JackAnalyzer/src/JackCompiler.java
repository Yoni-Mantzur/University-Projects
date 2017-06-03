import java.io.File;
import java.io.IOException;
/**
 * 
 * @author Yoni
 *
 */
public class JackCompiler {
	
	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		
		File fileName = new File(args[0]);		
		File files[] = fileName.listFiles();
		
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
				
				int index = path.lastIndexOf("jack");
				if (index == -1)
					continue;
				
				String newPath = path.substring(0, index) + "vm";
				
				CompilationEngine compilationEngine = new CompilationEngine(path, newPath);
			
				compilationEngine.compileClass();
				
			}
		}
		
	}
	


}
