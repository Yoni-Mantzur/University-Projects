package oop.ex4.data_structures;


/**
 * Singleton Merge Sort.
 */
public class MergeSort {

    private static int[] helper;
    private static int[] numbers;

    /**
     * Sort method. Receives int array and sorts them.
     * @param values int[] - int array to sort.
     */
    public static void sort(int[] values) {
        if (values == null){  // null
            return;
        }
        try{
            numbers = values;
        }catch (ArrayStoreException e){  // In-case user tried to put other input type than int.
            return;
        }
        int number = values.length;
        helper = new int[number];
        mergeSort(0, number - 1);
    }

    private static void mergeSort (int start, int end) {
        // check if start is smaller then end, if not then the array is sorted
        if (start < end) {
            // Get the index of the element which is in the middle
            int middle = start + (end - start) / 2;
            // Sort the left side of the array
            mergeSort(start, middle);
            // Sort the right side of the array
            mergeSort(middle + 1, end);
            // Combine them both
            merge(start, middle, end);
        }
    }

    private static void merge(int start, int middle, int end) {

        // Copy both parts into the helper array
        System.arraycopy(numbers, start, helper, start, end + 1 - start);

        int i = start;
        int j = middle + 1;
        int k = start;
        // Copy the smallest values from either the left or the right side back
        // to the original array
        while (i <= middle && j <= end) {
            if (helper[i] <= helper[j]) {
                numbers[k] = helper[i];
                i++;
            } else {
                numbers[k] = helper[j];
                j++;
            }
            k++;
        }
        // Copy the rest of the left side of the array into the target array
        while (i <= middle) {
            numbers[k] = helper[i];
            k++;
            i++;
        }

    }
}
