package ex3;

import java.util.HashSet;
import java.util.LinkedList;
import java.util.TreeSet;

/**
 * Analyzes the qualities of each data structure.
 * @author YONI
 *
 */
public class SimpleSetPerformanceAnalyzer {
	
	private static final long TO_MS = 1000000;
	private static final int NUMBER_OF_STRUCTERS = 5;
	
	
	/**
	 * 
	 * check the insertion time of given structure and data list.
	 * @param structure - the structure to check-
	 * @param data - the data list to insert
	 * @return - the time it was took in Ns
	 */
	private static long insertData(SimpleSet structure, String[] data){
		
		long timeClaculateStart = System.nanoTime();
		
		for (int i = 0; i<data.length; i++){
			
			structure.add(data[i]);
		}
		
		long timeClaculateEnd = System.nanoTime();
		return (timeClaculateEnd - timeClaculateStart);
		
	}
	
	private static SimpleSet[] initalize(){
		
		SimpleSet[] dataStructers = new SimpleSet[NUMBER_OF_STRUCTERS];
		dataStructers[0] = new ChainedHashSet();
		dataStructers[1] = new OpenHashSet();			
		dataStructers[2] = new CollectionFacadeSet(new TreeSet<String>());
		dataStructers[3] = new CollectionFacadeSet(new LinkedList<String>());
		dataStructers[4] = new CollectionFacadeSet(new HashSet<String>());
		
		return dataStructers;
	}
	
	
	/*
	 * 
	 * check the contained value time of given structures.
	 * @param structure - the structure to check 
	 * @param value - the value check.
	 * @return - the time it was took in Ns.
	 */
	private static long containWord(SimpleSet structure, String value){
		
		long timeClaculateStart = System.nanoTime();
		
		structure.contains(value);
		
		long timeClaculateEnd = System.nanoTime();
		
		return (timeClaculateEnd - timeClaculateStart);
		
	}
	
	
	/*
	 * Check the results and print the winner
	 * @param namesStructures - the structures names
	 * @param results - the results
	 * @param competition - what competition
	 */
	private static void printResults (String[] namesStructures, long[] results, String competition){
		
		long winner = results[0];
		int iWinner = 0;
		
		for (int i = 1; i<results.length; i++){
			
			if (winner < results[i]){
				winner = results[i];
				iWinner = i;	
			}
		}
		
		System.out.println("The winner in "+ competition+" is: " +  
				namesStructures[iWinner] +"with: " + winner);
	}
	

	/*
	 * The function check several structures and their abilities.
	 * 
	 * @param structures - the structures we wants to test
	 * @param namesOfstructesrs - the names of the structures
	 * @param data - the data we want to put in
	 * @param tests - the tests
	 */
	private static void testStructer(SimpleSet[] structures, String[] namesOfstructesrs,
																	String[] data, String[] tests){
		
		
		long[] results = new long[NUMBER_OF_STRUCTERS];
		
		for (int k=0; k<tests.length; k++){

			System.out.println(tests[k] + ":");
			
			long time = 0;
			for (int i=0; i<NUMBER_OF_STRUCTERS; i++){
				if (k==0){
					time = SimpleSetPerformanceAnalyzer.insertData(structures[i], data)/TO_MS;
					System.out.println(namesOfstructesrs[i] + ": " + time +"Ms");
				} else {
					time = SimpleSetPerformanceAnalyzer.containWord(structures[i], tests[k]);
					System.out.println(namesOfstructesrs[i] + ": " + time +"Ns");
				}
				results[i] = time;
			}
			
			printResults(namesOfstructesrs, results, tests[k]+" for data1: ");
			
		}
		
	}
	public static void main(String[] args) {
			
		SimpleSet[] dataStructers = initalize();
			
		String[] namesStucters = {"ChainedHashSet", "OpenHashSet", "TreeSet", "LinkedList", "HashSet"};
		
		String[] data1 = Ex3Utils.file2array("data1.txt");
		String[] data2 = Ex3Utils.file2array("data2.txt");
		
		String[] testsForData1 = {"insertion" ,"contain hi", "contain -13170890158"};
		String[] testsForData2 = {"insertion" ,"contain 23" ,"contain hi"};
		
		
		//Print the results of data1 and data 2
		
		//For data 1	
		testStructer(dataStructers, namesStucters, data1, testsForData1);
		
		//For data 2
		testStructer(dataStructers, namesStucters, data2, testsForData2);
	}
}