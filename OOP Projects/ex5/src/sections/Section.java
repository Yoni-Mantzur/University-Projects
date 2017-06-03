package sections;

import filters.*;
import orders.*;


/**
 * Class represent a Section from the CommandFile.
 * 
 * @author YONI
 * @see Order
 * @see Filter
 */
public class Section {
	
	/* The filter of the section */
	private final Filter FILTER;
	/* The order of the section */
	private final Order ORDER;
	/* Warning array */
	int warningFilter, warningOrder;

	/**
	 * Constructor.
	 * 
	 * @param filterOfSecion - the filter of this section.
	 * @param orderOfSection - the order of this section
	 */
	public Section(Filter filterOfSecion, Order orderOfSection, int warningFilter, int warningOrder) {
		
		FILTER = filterOfSecion;
		ORDER = orderOfSection;
		this.warningFilter = warningFilter;
		this.warningOrder = warningOrder;
	}
	
	/**
	 * @return the filter of this section.
	 */
	public Filter getFilter(){
		return FILTER;
	}
	
	/**
	 * @return the order of this section.
	 */
	public Order getOrder(){
		
		return ORDER;
	}
	
	/**
	 * @return the lines have been warnings.
	 */
	public int getFilterWarning(){
		
		return warningFilter;
	}
	
	
	/**
	 * @return the lines have been warnings.
	 */
	public int getOrderWarning(){
		
		return warningOrder;
	}


}
