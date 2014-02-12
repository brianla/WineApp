package cse110;

import java.io.File;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashSet;

import util.PutnSet;

import csv.CSV;
import csv.CSVRow;


public class TopNRecommenderTest implements Runnable{
	
	private static final File vectorFile = new File("WineVectors_CSV.csv");
	
	private final int n_TopRecommended = 5;
	private final int k_RandomWines = 10;
	private final double c_typeScalar = 0.1;
	private final double c_varietalScalar = 0.1;
	
	private final boolean DEBUG = false;
	
	/********************************************************************
	 * Run Top-N Recommender Test
	 ********************************************************************/
	@Override
	public void run() 
	{
		System.out.println("Loading Wine Vector Data");
		CSV data = new CSV();
		data.loadCSVSpreadsheet(vectorFile);

		System.out.println("Running Test: Retrieving Top-" + n_TopRecommended + " wines for " + k_RandomWines + " random wines.");
		runTest1(data);
	}
	
	/********************************************************************
	 * Calculation Methods
	 ********************************************************************/	
	private void runTest1(CSV data)
	{
		HashSet<Integer> randomIndicies = getRandomK(0, data.getRows().size(), k_RandomWines);
		
		CSVRow row_i = null;
		for(Integer i : randomIndicies)
		{
			row_i = data.getRows().get(i);
			ArrayList<Pair<CSVRow, Double>> pairs = generatePairs(data, row_i, i);
			pairs = getSortedDistances(pairs);
			
			System.out.println("Wine: " + row_i.getValueByKey(Keys.id)
					+ ", " + row_i.getValueByKey(Keys.winename)
					+ ", " + row_i.getValueByKey(Keys.winery));
			
			System.out.println("Top-" + n_TopRecommended + ": ");
			for(int j = 0; j < n_TopRecommended && j < pairs.size(); j++)
			{
				System.out.println("\tWine: " + col("Dist: " + pairs.get(j).second, 15) 
						+ " Vector: " + pairs.get(j).first.getValueByKey(Keys.id)
						+ ", " + pairs.get(j).first.getValueByKey(Keys.winename)
						+ ", " + pairs.get(j).first.getValueByKey(Keys.winery));
			}
			System.out.println();
		}
		
	}
	
	private ArrayList<Pair<CSVRow, Double>> generatePairs(CSV data, CSVRow row_i, int i)
	{
		ArrayList<Pair<CSVRow, Double>> pairs = new ArrayList<Pair<CSVRow, Double>>();
		CSVRow row = null;
		double dist = -1.0;
		Pair<CSVRow, Double> pair = null;
		for(int r = 0; r < data.getRows().size(); r++)
		{
			if(i == r)
				continue;
			row = data.getRows().get(r);
			dist = getSquaredDistance(row_i, row);
			pair = new Pair<CSVRow, Double>(row, dist);
			pairs.add(pair);
		}
		
		return pairs;
	}
	
	//Max is non-inclusive!
	private HashSet<Integer> getRandomK(int min, int max, int k)
	{
		HashSet<Integer> ints = new HashSet<Integer>();
		while(--k >= 0)
			ints.add(  (int)Math.floor(min + (max-min)*Math.random())  );
		return ints;
	}
	
	private double getSquaredDistance(CSVRow row_i, CSVRow row)
	{
		double dist = 0.0;
		for(String key : Keys.aromas)
			dist += Math.pow(  (new Double(row_i.getValueByKey(key)) - new Double(row.getValueByKey(key)))  , 2.0);
		dist += (wineType(row_i).equals(wineType(row))) ? 0 : c_typeScalar;
		dist += (wineVarietal(row_i).equals(wineVarietal(row))) ? 0 : c_varietalScalar;
		return dist;
	}
	
	private String wineType(CSVRow row)
	{
		return (row.getValueByKey(Keys.type).toLowerCase().trim());
	}
	
	private String wineVarietal(CSVRow row)
	{
		return (row.getValueByKey(Keys.varietal).toLowerCase().trim());
	}
	
	
	/********************************************************************
	 * Helper Methods
	 ********************************************************************/
	
	private String col(String str, int width)
	{
		String fixedStr;
		if(str.length() > width) {
			fixedStr = str.substring(0, width);
		}else{
			int diff = width-str.length();
			fixedStr = new String(str);
			for(int i = 0; i < diff; i++)
				fixedStr += " ";
		}
		return fixedStr;
	}
	
	
	private ArrayList<Pair<CSVRow, Double>> getSortedDistances(ArrayList<Pair<CSVRow, Double>> rows)
	{
		ArrayList<Pair<CSVRow, Double>> sorted = new ArrayList<Pair<CSVRow, Double>>();
		Pair<CSVRow, Double> current;
		for(int i = 0; i < rows.size(); i++)
		{
			current = rows.get(i);
			for(int j = sorted.size(); j >= 0; j--)
			{
				if(j != 0 && current.second < sorted.get(j-1).second)
					continue;
				if(j == sorted.size())
					sorted.add(current);
				else
					sorted.add(j, current);
				break;
			}
		}
		return sorted;
	}
	
	/********************************************************************
	 * Private Classes
	 ********************************************************************/

	/**
	 * A generic Pair for use in associating two values
	 */
	private class Pair<T,U>
	{
		public T first;
		public U second;
		
		public Pair() {
			this(null, null);
		}
		
		public Pair(T first, U second) {
			this.first = first;
			this.second = second;
		}
		
		public String toString() {
			return "<" + first.toString() + "," + second.toString() + ">";
		}
	}
	
	public static class Keys
	{
		public static final LinkedHashSet<String> set = new LinkedHashSet<String>();
		public static final LinkedHashSet<String> aromas = new LinkedHashSet<String>();
		public static final String id = PutnSet.add(set, "wineID");
		public static final String winery = PutnSet.add(set, "winery");
		public static final String winename = PutnSet.add(set, "wineName");
		public static final String ava = PutnSet.add(set, "ava");
		public static final String vintage = PutnSet.add(set, "vintage");
		public static final String price = PutnSet.add(set, "price");
		public static final String rating = PutnSet.add(set, "rating");
		public static final String notes = PutnSet.add(set, "notes");
		public static final String region = PutnSet.add(set, "region");
		public static final String type = PutnSet.add(set, "type");
		public static final String varietal = PutnSet.add(set, "varietal");
		public static final String bitter = PutnSet.add(aromas, PutnSet.add(set, "bitter"));
		public static final String sweet = PutnSet.add(aromas, PutnSet.add(set, "sweet"));
		public static final String sour = PutnSet.add(aromas, PutnSet.add(set, "sour"));
		public static final String salty = PutnSet.add(aromas, PutnSet.add(set, "salty"));
		public static final String chemical = PutnSet.add(aromas, PutnSet.add(set, "chemical"));
		public static final String pungent = PutnSet.add(aromas, PutnSet.add(set, "pungent"));
		public static final String oxidized = PutnSet.add(aromas, PutnSet.add(set, "oxidized"));
		public static final String microbio = PutnSet.add(aromas, PutnSet.add(set, "microbiological"));
		public static final String floral = PutnSet.add(aromas, PutnSet.add(set, "floral"));
		public static final String spicy = PutnSet.add(aromas, PutnSet.add(set, "spicy"));
		public static final String fruity = PutnSet.add(aromas, PutnSet.add(set, "fruity"));
		public static final String vege = PutnSet.add(aromas, PutnSet.add(set, "vegetative"));
		public static final String nutty = PutnSet.add(aromas, PutnSet.add(set, "nutty"));
		public static final String caramel = PutnSet.add(aromas, PutnSet.add(set, "caramelized"));
		public static final String woody = PutnSet.add(aromas, PutnSet.add(set, "woody"));
		public static final String earthy = PutnSet.add(aromas, PutnSet.add(set, "earthy"));
	}
	
	/********************************************************************
	 * Main
	 ********************************************************************/
	public static void main(String[] args)
	{
		TopNRecommenderTest test = new TopNRecommenderTest();
		System.out.println("Main(): Begin running Top-N Recommender Test...");
		test.run();
		System.out.println("Main(): Finished running Top-N Recommender Test.");
	}
}