/**
 * This class implements the FIFO page-replacement strategy.
 */

public class FIFO extends ReplacementAlgorithm {
    // FIFO list of page frames
    private FIFOList frameList;

    /**
     * @param pageFrameCount - the number of physical page frames
     */
    public FIFO(int pageFrameCount) {
        super(pageFrameCount);
        frameList = new FIFOList(pageFrameCount);
    }


    /**
     * insert a page into a page frame.
     *
     * @param pageNumber - the page number being inserted.
     */
    public void insert(int pageNumber) {
        frameList.insert(pageNumber);
    }

    class FIFOList {
        // the page frame list
        int[] pageFrameList;

        // the number of elements in the page frame list
        //firstIn index
        int firstIndex = 0;

        FIFOList(int pageFrameCount) {
            pageFrameList = new int[pageFrameCount];

            // we initialize each entry to -1 to indicate initial value is invalid 
            java.util.Arrays.fill(pageFrameList, -1);
        }

        /**
         * @param pageNumber the number of the page to be
         *                   inserted into the page frame list.
         */
        void insert(int pageNumber) {
            //TODO: insert code here
            //fault flag
            boolean flag;
            flag = search(pageNumber);
            if (!flag) {
                pageFrameList[firstIndex] = pageNumber;
                firstIndex++;
                if (firstIndex == pageFrameList.length) {
                    firstIndex = 0;// back to the head of frame
                }
                System.out.print("frame: ");
                for (int j = 0; j < pageFrameList.length; j++) {
                    if (pageFrameList[j] != -1) {
                        System.out.print(pageFrameList[j] + "   ");
                    } else
                        System.out.print("    ");
                }
                System.out.print(" --> page fault!");

                System.out.println();
                pageFaultCount++;
            }
            //page hit
            else {
                System.out.print("frame: ");
                /* display the frame buffer array */
                for (int j = 0; j < pageFrameList.length; j++) {
                    if (pageFrameList[j] != -1) {
                        System.out.print(pageFrameList[j] + "   ");
                    } else
                        System.out.print("    ");
                }
                System.out.print(" --> page hit!");
                System.out.println();
            }
        }

        /**
         * Searches for page pageNumber in the page frame list
         * @return false if pageNumber was not found
         */
        boolean search(int pageNumber) {
            boolean returnVal = false;

            for (int i = 0; i < pageFrameList.length; i++) {
                if (pageNumber == pageFrameList[i]) {
                    returnVal = true;
                    break;
                }
            }
            return returnVal;
        }
    }
}
