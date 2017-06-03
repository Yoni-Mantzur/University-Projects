package oop.ex5.filescript;


import java.io.*;
import java.util.*;
import sections.*;

/**
 * Class get directory and commend file and prints the files relevant each section.
 * 
 * @see Section
 * @see ParsingFile
 * @see OneTypeException 
 * @see SecondTypeException
 * @author YONI
 *
 */
public class MyFileScript {
	
	/* Represent Second type error */
	private static final String STDERR = "ERROR";
	/**/
	private static final int LEGAL_NUMBER_ARGUMMENTS = 2, DIRECTORY = 0, COMMEND_FILE = 1;
	static final int NO_WARNING = -1;
	
	/* Create list of files in given directory */
	private static ArrayList<File> getFiles(File SourceDir){
		
		ArrayList<File> listOfFiles = new ArrayList<>();
		
		for (File itemInDirectory : SourceDir.listFiles()){
			
			if (itemInDirectory.isFile())
				listOfFiles.add(itemInDirectory);
		}
		
		return listOfFiles;
		
	}

	/**
	 * Get directory and commend file and prints the files relevant each section.
	 * 
	 * @param args - Contains two paths - the first sourceDirectory and second the commendFile.
	 */
	public static void main(String[] args){
				
		try{
			if (args.length != LEGAL_NUMBER_ARGUMMENTS)
				throw new SecondTypeException();
			
			File SourceDirectory = new File(args[DIRECTORY]), commendFile = new File(args[COMMEND_FILE]);
			ArrayList<File> filesInDirectory = getFiles(SourceDirectory);
			for (File file : filesInDirectory){
				
				if (file.isFile() && file.canWrite())
					System.out.println(file.getName());
			}
			
			BufferedReader fileToParse = new BufferedReader(new FileReader(commendFile));
			
			// Get all the sections from commend file, using ParsingFile.
			ArrayList<Section> sections = ParsingFile.getSections(fileToParse);
			
			for (Section section : sections){
				
				ArrayList<File> filesOfSection = new ArrayList<>();
				
				// Prints warnings.
				if (section.getFilterWarning() != NO_WARNING)
					System.err.println("warning in line " + section.getFilterWarning());
				if (section.getOrderWarning() != NO_WARNING)
					System.err.println("warning in line " + section.getOrderWarning());
				
				for (File file : filesInDirectory)
					if (section.getFilter().filterDirectory(file))
						filesOfSection.add(file);
				
				// Sort with order of current section.
				Collections.sort(filesOfSection, section.getOrder());
				for (File file : filesOfSection)
					if (file != null)
						System.out.println(file.getName());
				
			}
		// If second exception prints to error.
		} catch (SecondTypeException | IOException exception){
			
			System.err.println( STDERR );
		}
	}

}













/*
package filescript;

import java.io.*;

import filters.*;
import orders.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.NoSuchElementException;

import sections.*;


 * Class represent a parsing Commends File.
 * 
 * @author YONI
 *
 
class ParsingFile{

	 Represent separating character in commend file 
	private static final String SPERATING_COMMEND = "#";
	
	
	private BufferedReader fileToParse;
	private String currentCommendLine, lastCommendLine;
	private int numberLine;
	private ArrayList sections;
	



	public ParsingFile(File fileToParse) throws SecondTypeException{
		try{
			this.fileToParse = new BufferedReader(new FileReader(fileToParse));		
			this.currentCommendLine = this.fileToParse.readLine();
			this.lastCommendLine = Order.ORDER_REPRESENTATION;
			this.numberLine = 0;
			
		} catch (IOException exception){
			throw new SecondTypeException();
		}
	}
		
			
	public static ArrayList<Section> getSections(BufferedReader fileToParse2) {
		// TODO Auto-generated method stub
		return null;
	}


	 Find the commend line for filter 
	private String[] findFilter(String commendLine) throws SecondTypeException{
		try{
			if (this.currentCommendLine == Filter.FILTER_REPRESENTION && 
														this.lastCommendLine == Order.ORDER_REPRESENTATION){
				this.numberLine++;
				String filterParamenters = this.fileToParse.readLine();
				this.lastCommendLine = Filter.FILTER_REPRESENTION;
				return filterParamenters.split(SPERATING_COMMEND);
			}
			
			throw new SecondTypeException();
			
		} catch (IOException exception){			
			throw new SecondTypeException();	
		}
	}
	
	Find the commend line for order 
	private String[] findOrder(String commendLine) throws SecondTypeException{
		
		try{
		
			this.currentCommendLine = this.fileToParse.readLine();
			this.numberLine++;
		
			if (this.currentCommendLine == Order.ORDER_REPRESENTATION && 
														this.lastCommendLine == Filter.FILTER_REPRESENTION){
		
				this.numberLine++;
				String filterParamenters = this.fileToParse.readLine();
				this.lastCommendLine = Order.ORDER_REPRESENTATION;
				return filterParamenters.split(SPERATING_COMMEND);
			}
		
				throw new SecondTypeException();	
				
			} catch (IOException exception){			
				throw new SecondTypeException();	
			}
	}
	
		
		try{
			String[] filterParameters = findFilter(this.currentCommendLine);
		
			int lengthParameters = filterParameters.length-1;
			String nameFilter = filterParameters[0], NegativeParameter = filterParameters[lengthParameters];
		
			return FilterFactory.createFilter(nameFilter, 
				Arrays.copyOfRange(filterParameters, 1, lengthParameters), NegativeParameter);
			
	}
	

	private Order creatOrder() throws OneTypeException, SecondTypeException{
		try{
			String[] orderParameters = findOrder(this.currentCommendLine);
		
			String nameOrder = orderParameters[0], isReverse = 
					(orderParameters.length > 1) ? orderParameters[1] : null;
				
					return OrderFactory.createOrder(nameOrder, isReverse);
		
	}

	

	public Section[] getSections(){		

		while (this.currentCommendLine != null){
			
			try{
				Filter filterOfSection = creatFilter();
			

			
			Order orderOfSection = creatOrder();
			
			this.currentCommendLine = this.fileToParse.readLine();
			if (this.currentCommendLine == null)
				throw new SecondTypeException();
			this.numberLine++;
			
			return new Section(filterOfSection, orderOfSection);
	}*/