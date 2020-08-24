/**
 * This class implements the LRU page-replacement strategy.
 */

public class LRU extends ReplacementAlgorithm {
    // LRU list of page frames
    private LRUList frameList;

    /**
     * @param pageFrameCount - the number of physical page frames
     */
    public LRU(int pageFrameCount) {
        super(pageFrameCount);
        frameList = new LRUList(pageFrameCount);
    }

    /**
     * Insert a page into a page frame.
     */
    public void insert(int pageNumber) {
        frameList.insert(pageNumber);
    }

    class LRUList {
        // the page frame list
        int[] pageFrameList;

        //least recently
        int LRIndex = 0;

        //sort[] stores the sorted list of pages from most recently used to least recently used
        //temp[] is the temporary array used to update the list
        int[] sort;
        int[] temp;

        LRUList(int pageFrameCount) {
            pageFrameList = new int[pageFrameCount];

            // we initialize each entry to -1 to indicate initial value is invalid.
            java.util.Arrays.fill(pageFrameList, -1);
            sort = new int[pageFrameCount];
            temp = new int[pageFrameCount];
            for (int i = 0; i < pageFrameCount; i++) {
                sort[i] = -1;
                temp[i] = -1;
            }
        }

        /**
         * @param pageNumber the number of the page to be
         *                   inserted into the page frame list.
         */
        void insert(int pageNumber) {
            //TODO: insert code here
            //fault flag
            //-1 is page fault
            int flag;
            flag = search(pageNumber);


            //page fault, get the least used index
            for (int j = 0; j < pageFrameCount && flag == -1; j++) {
                if (pageFrameList[j] == sort[pageFrameCount - 1]) {
                    LRIndex = j;
                    break;
                }
            }

            //page fault, replace the least recently used page
            if (flag == -1) {
                pageFrameList[LRIndex] = pageNumber;
                System.out.print("frame: ");
                /* display frame buffer array */
                for (int j = 0; j < pageFrameList.length; j++) {
                    if (pageFrameList[j] != -1) {
                        System.out.print(pageFrameList[j] + "   ");
                    } else
                        System.out.print("    ");
                }
                System.out.println(" --> page fault!");
                pageFaultCount++;
            }
            //page hit
            else {
                /* display frame buffer array */
                System.out.print("frame: ");
                for (int j = 0; j < pageFrameList.length; j++) {
                    if (pageFrameList[j] != -1) {
                        System.out.print(pageFrameList[j] + "   ");
                    } else
                        System.out.print("    ");
                }
                System.out.println(" --> page hit!");
            }

            /** update MRU-LRU array */
            // use temp[] to temporarily store the array
            // first element of temp[] is the newly inserted page
            int p = 1;
            temp[0] = pageNumber;
            for (int j = 0; j < sort.length; j++) {
                //the elements in sort[] that are not equal to referenced page
                //or is not the most recently used
                if (!(pageNumber == sort[j]) && p < pageFrameList.length) {
                    temp[p] = sort[j];
                    p++;
                }
            }
            //update sort[]
            for (int j = 0; j < pageFrameList.length; j++) {
                sort[j] = temp[j];
            }
        }

        /**
         * Searches for page pageNumber in the page frame list
         * @return -1 if pageNumber was not found
         */
        int search(int pageNumber) {
            int returnVal = -1;

            for (int i = 0; i < pageFrameList.length; i++) {
                if (pageNumber == pageFrameList[i]) {
                    returnVal = i;
                    break;
                }
            }
            return returnVal;
        }
    }
}
