package filters;

import java.io.File;

/**
 * Represent an "all"  (means pass all) Filter.
 * @author YONI
 *
 */
public class AllFilesFilter implements Filter {

	/** Filter Name */
	static final String NAME_FILTER = "all";
	
	
	@Override
	public boolean filterDirectory(File fileToCheack) {
		return true;
	}

}
