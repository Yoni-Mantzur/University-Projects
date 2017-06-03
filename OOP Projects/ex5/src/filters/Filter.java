package filters;

import java.io.File;


/**
 * A filter of files.
 * 
 * @author YONI
 *
 */
public interface Filter{
	/** Filter Name */
	public final String FILTER_REPRESENTION = "FILTER";
	
	/**
	 * Filter the files in given directory.
	 * 
	 * @param fileToCheack - A file to filter.
	 * @return - a true if file traversed the filter.
	 */
	public boolean filterDirectory(File fileToCheack);

	
}
