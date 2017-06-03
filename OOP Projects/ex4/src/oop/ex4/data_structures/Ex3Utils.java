package oop.ex4.data_structures;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

/**
 * A utilities class. made by OOP staff edited by Ben Asaf.
 *
 * LAST UPDATED: 15/5/2015 00:30 PM
 * VERSION: V1.3
 */
public class Ex3Utils {

	public static String[] fileToLines(String fileName) {
		// A list to hold the file's content
		List<String> fileContent = new ArrayList<String>();

		// Reader object for reading the file
		BufferedReader reader = null;

		try {
			reader = new BufferedReader(new FileReader(fileName));  // Open a reader
			String line = reader.readLine();
			// Go over the rest of the file
			while (line != null) {
				// Read the next line
				fileContent.add(line);
				line = reader.readLine();
			}

		} catch (FileNotFoundException e) {
			System.err.println("ERROR: The file: " + fileName + " is not found.");
			return null;
		} catch (IOException e) {
			System.err.println("ERROR: An IO error occurred.");
			return null;
		} finally {
			// Try to close the file
			try {
				if(reader != null)
					reader.close();
				else
					return null;
			} catch (IOException e) {
				System.err.println("ERROR: Could not close the file " + fileName + ".");
			}
		}

		// Convert the list to an array and return the array
		String[] result = new String[fileContent.size()];
		fileContent.toArray(result);
		return result;
	}

	/**
	 * Reads a text file (such that each line contains a single word), 
	 * and returns a string array of its lines.
	 * @param fileName Text file to read.
	 * @return Array with the file's content (returns null if the IOException occurred).
	 */
	public static String[] fileToWords(String fileName) {
		// A list to hold the file's content
		List<String> fileContent = new ArrayList<String>();

		// Reader object for reading the file
		BufferedReader reader = null;

		try {
			reader = new BufferedReader(new FileReader(fileName));  // Open a reader
			String line = reader.readLine();
			// Go over the rest of the file
			while (line != null) {
				String[] words = line.split(" ");
				for (int i = 0; i < words.length; i++) {
					// You may want to check for a non-word character before blindly
					// performing a replacement
					// It may also be necessary to adjust the character class
					fileContent.add(words[i]);
				}
				line = reader.readLine();

				// Read the next line
			}

		} catch (FileNotFoundException e) {
			System.err.println("ERROR: The file: " + fileName + " is not found.");
			return null; 
		} catch (IOException e) {
			System.err.println("ERROR: An IO error occurred.");
			return null; 
		} finally {
			// Try to close the file
			try {
				if(reader != null)
					reader.close();
				else
					return null;
			} catch (IOException e) {
				System.err.println("ERROR: Could not close the file " + fileName + ".");
			}
		}

		// Convert the list to an array and return the array
		String[] result = new String[fileContent.size()];
		fileContent.toArray(result);
		return result;
	}
}
