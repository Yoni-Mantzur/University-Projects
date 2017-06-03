package orders;

import java.io.File;
import java.util.Comparator;

/**
 * Interface of Order implements Comparator<File>.
 * 
 * @author YONI
 *
 */
public interface Order extends Comparator<File>{
	
	/** Name of Order */
	public static String ORDER_REPRESENTATION = "ORDER" ;

}
