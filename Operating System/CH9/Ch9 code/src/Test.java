/**
 * Test harness for LRU and FIFO page replacement algorithms
 *
 * Usage:
 *	java [-Ddebug] Test <reference string size> <number of page frames>
 */

public class Test
{
	public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: java Test <reference string size> <number of page frames>");
            System.exit(-1);
        }

        //arg[0] is the reference string size
		PageGenerator ref = new PageGenerator(new Integer(args[0]).intValue());
        //generate referenceString
		int[] referenceString = ref.getReferenceString();

		//arg[1] is the number of page frames
		/** Use either the FIFO or LRU algorithms */

		System.out.println( "************************" );
		System.out.println( "          FIFO" );
		System.out.println( "************************" );
		ReplacementAlgorithm fifo = new FIFO(new Integer(args[1]).intValue());
		// output a message when inserting a page
		for (int i = 0; i < referenceString.length; i++) {
			//System.out.println("inserting " + referenceString[i]);
			fifo.insert(referenceString[i]);
		}
		System.out.println("FIFO faults = " + fifo.getPageFaultCount());


		System.out.println( "************************" );
		System.out.println( "          LRU" );
		System.out.println( "************************" );
		ReplacementAlgorithm lru = new LRU(new Integer(args[1]).intValue());
		// output a message when inserting a page
		for (int i = 0; i < referenceString.length; i++) {
			//System.out.println("inserting " + referenceString[i]);
			lru.insert(referenceString[i]);
		}
		// report the total number of page faults
		System.out.println("LRU faults = " + lru.getPageFaultCount());
	}
}
