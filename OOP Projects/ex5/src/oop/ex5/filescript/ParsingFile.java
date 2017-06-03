package oop.ex5.filescript;

import java.io.*;

import filters.*;
import orders.*;

import java.util.ArrayList;
import java.util.Arrays;

import sections.*;

/**
 * Class represent a parsing Commends File.
 * 
 * @see Section
 * @see MyFileScript
 * @author YONI
 *
 */
public class ParsingFile{
	

	/* Represent separating character in commend file */
	private static final String SPERATING_COMMEND = "#";
	
	/* Represent the number of lines number read*/
	private static final int ONE_MORE_LINE = 1, TWO_MORE_LINES = 2;
	
	/* Create Filter using the commend lines */
	private static Filter createFilter(String currentLine, String nextLine, String last_subSection) 
															throws OneTypeException, SecondTypeException{
		
		// Error with commend line section.
		if (!currentLine.equals(Filter.FILTER_REPRESENTION))
			throw new SecondTypeException();
				
		if (nextLine.equals(Order.ORDER_REPRESENTATION))
			return null;
		
		String[] arrayLine = nextLine.split(SPERATING_COMMEND);
		
		// Create and return filter with the name of the filter in place one.
		return FilterFactory.createFilter(arrayLine[0], 
				Arrays.copyOfRange(arrayLine, 1, arrayLine.length), arrayLine[arrayLine.length -1]);
	}

	/*  Create Order using the commend lines */
	private static Order createOrder(String currentLine, String nextLine, String last_subSection) 
															throws OneTypeException, SecondTypeException{
		// Error with commend line section.
		if (!currentLine.equals(Order.ORDER_REPRESENTATION))
			throw new SecondTypeException();
		
		if (nextLine == Filter.FILTER_REPRESENTION)
			return null;
		
		String[] arrayLine = nextLine.split(SPERATING_COMMEND);
		
		// Create and return order with the name of the filter in place one.
		return OrderFactory.createOrder(arrayLine[0], (arrayLine.length > 1)? arrayLine[1] : null);
					
					
	}
	
	/**
	 * Static method that get Commend file and parse it to sections.
	 * 
	 * @param fileToParse - the commend file to parse.
	 * @return listArray of sections.
	 * @throws SecondTypeException - throws SecondTypeException if some standard error occurred
	 * @throws IOException - if the read from file throws error.
	 */
	public static ArrayList<Section> getSections(BufferedReader fileToParse) throws SecondTypeException, 
																								IOException{
		
		ArrayList<Section> sections = new ArrayList<>();
		int lineNumber = TWO_MORE_LINES;
		String currentLine = fileToParse.readLine(), nextLine = fileToParse.readLine(),
													 last_subSection = Order.ORDER_REPRESENTATION;
		Order order;
		Filter filter;
		
		// flag if some commendLine without parameters.
		boolean isLineEmpty = false;
															
		while (currentLine != null){ // While not end of file.

			int warningFilter = MyFileScript.NO_WARNING, warningOrder = MyFileScript.NO_WARNING;
			// try to create filter.			
			try{
				
				filter = createFilter(currentLine, nextLine, last_subSection);
				isLineEmpty = (filter == null)? true : false;		
				
			} catch (OneTypeException exception){
				//Default filter.
				filter = FilterFactory.createFilter();
				warningFilter = lineNumber;				
			}
			// Check if parameters line was empty, if not move to next line.
			currentLine = (isLineEmpty == true)? nextLine : fileToParse.readLine();
			nextLine =  fileToParse.readLine();
			lineNumber = (isLineEmpty == true)?  lineNumber+ONE_MORE_LINE : lineNumber+TWO_MORE_LINES;
			last_subSection = Filter.FILTER_REPRESENTION;
					
			try{
				order = createOrder(currentLine, nextLine, last_subSection);
				isLineEmpty = (order == null)? true : false;
					
			} catch (OneTypeException exception){
				
				order = OrderFactory.createOrder();
				warningOrder = lineNumber;				
			}
			// Create section given the commend lines of sub-section.
			sections.add(new Section(filter, order, warningFilter, warningOrder));
			
			// Check if parameters line was empty, if not move to next line.
			currentLine = (isLineEmpty == true)? nextLine : fileToParse.readLine();
			nextLine =  fileToParse.readLine();
			lineNumber = (isLineEmpty == true)?  lineNumber+ONE_MORE_LINE : lineNumber+TWO_MORE_LINES;
			last_subSection = Order.ORDER_REPRESENTATION;	
			
		}
		
		return sections;
					
	}

}
