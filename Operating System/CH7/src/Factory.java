/**
 * A factory class that creates (1) the bank and (2) each customer at the bank.
 *
 * Usage:
 *	java Factory <one or more resources>
 *
 * I.e.
 *	java Factory 10 5 7
 */

import java.io.*;
import java.util.*;

public class Factory
{
	public static void main(String[] args) {
        int numOfResources = args.length;
		int[] resources = new int[numOfResources];

		// initialize resources with the args[]
		for (int i = 0; i < numOfResources; i++)
			resources[i] = Integer.parseInt(args[i].trim());

		// initialized bank with resources[]
		Bank theBank = new BankImpl(resources);
		// array of max demand
        int[] maxDemand = new int[numOfResources];

        // initialize the customers
        Thread[] workers = new Thread[Customer.COUNT];
                
		// read initial values for maximum need array
		String line;
		try {
			BufferedReader inFile = new BufferedReader(new FileReader("/Users/xiaxi/Documents/操作系统/assignment/assignment CH7/Bank/src/infile.txt"));

			int threadNum = 0;
            int resourceNum = 0;

            for (int i = 0; i < Customer.COUNT; i++) {
                line = inFile.readLine();
                StringTokenizer tokens = new StringTokenizer(line,",");

                while (tokens.hasMoreTokens()) {
                    int amt = Integer.parseInt(tokens.nextToken().trim());
                    maxDemand[resourceNum++] = amt;
                }
                workers[threadNum] = new Thread(new Customer(threadNum, maxDemand, theBank));
                theBank.addCustomer(threadNum,maxDemand);
                //theBank.getCustomer(threadNum);
                ++threadNum;
                resourceNum = 0;
            }
		}
		catch (FileNotFoundException fnfe) {
			throw new Error("Unable to find file \"infile.txt\"");
		}
		catch (IOException ioe) {
			throw new Error("Error processing \"infile.txt\"");
		}

        System.out.println("FACTORY: created threads");

		// workers(Thread) starts
        for (int i = 0; i < Customer.COUNT; i++)
            workers[i].start();

        System.out.println("FACTORY: started threads");

        /**
         try { Thread.sleep(5000); } catch (InterruptedException ie) { }
         System.out.println("FACTORY: interrupting threads");
         for (int i = 0; i < Customer.COUNT; i++)
         workers[i].interrupt();
         */
        // start all the customers

	}
}
