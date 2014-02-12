package cse110;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;

import util.PutnSet;
import cse110.TopNRecommenderTest.Keys;
import csv.CSV;
import csv.CSVHeaderRow;
import csv.CSVRow;
import file.SimplePrinter;

public class WineReviewVectorGenerator implements Runnable {
	


	/*************************************************************************************
	 * Class Variables
	 *************************************************************************************/

	private final String vectorFileName = "TasteVectors.csv";
	private final String wineDBFileName = "WineTastingDB.csv";
	private final double DECAY_LAMBDA = 0.9;
	private final boolean DEBUG = true;
	private final boolean OUTPUT_TAB_SEPARATED = true;
	private final boolean OUTPUT_SQL_SCRIPT = true;
	private final boolean OUTPUT_CSV = true;


	/*************************************************************************************
	 * Run
	 *************************************************************************************/
	
	@Override
	public void run()
	{
		CSV vectors = loadCSV(vectorFileName);
		CSV db = loadCSV(wineDBFileName);
		
		System.out.println("Loading Word-to-TagVector Map...");
		HashMap<String,TagVector> wordToTVMap = buildWordToTagVectorMap(vectors);
		System.out.println("Total TagVectors: " + wordToTVMap.size()); 

		System.out.println("Loading Wine Vectors...");
		ArrayList<WineVector> wineVects = loadWineVectors(db);
		System.out.println("Total Wine Vectors: " + wineVects.size()); 

		System.out.println("Processing Wine Reviews into Feature Vectors...");
		processWineNotesIntoVectors(wineVects, wordToTVMap);
		
		normalizeWineVectors(wineVects);
		
		if(DEBUG)debugDumpWineVector(wineVects);

		if(OUTPUT_TAB_SEPARATED)outputTabSeparatedFile(wineVects);
		if(OUTPUT_SQL_SCRIPT)outputDatabaseScript(wineVects);
		if(OUTPUT_CSV)outputCSV(wineVects);
	}


	/*************************************************************************************
	 * Loading and Data Preparation Methods
	 *************************************************************************************/

	private CSV loadCSV(String fileName)
	{
		CSV csv = new CSV();
		csv.loadCSVSpreadsheet(new File(fileName));
		return csv;
	}
	
	private HashMap<String, TagVector> buildWordToTagVectorMap(CSV vectors)
	{
		HashMap<String, TagVector> map = new HashMap<String, TagVector>();
		
		CSVRow row = null;
		TagVector tv = null;
		for(int i = 0; i < vectors.getRows().size(); i++)
		{
			row = vectors.getRows().get(i);
			tv = new TagVector(row.getValueByKey(Constants.TagVector.word), row.getValueByKey(Constants.TagVector.key));
			tv.isDefining = (row.getValueByKey(Constants.TagVector.define) != null && !row.getValueByKey(Constants.TagVector.define).isEmpty());
			tv.effect = row.getValueByKey(Constants.TagVector.effect);
			for(String aroma : Constants.TagVector.aromas)
			{
				double aromaValue = 0.0;
				String strVal = null;
				try{
					strVal = row.getValueByKey(aroma);
					if(strVal == null || strVal.isEmpty())
						aromaValue = Double.NaN;
					else
						aromaValue = Double.parseDouble(strVal);
				}catch(Exception e){e.printStackTrace();}
				tv.descriptors.put(aroma, aromaValue);
			}
			
			map.put(tv.word, tv);
		}
		
		return map;
	}
	
	private ArrayList<WineVector> loadWineVectors(CSV db)
	{
		ArrayList<WineVector> vects = new ArrayList<WineVector>();
		
		WineVector wv = null;
		CSVRow row = null;
		for(int i = 0; i < db.getRows().size(); i++)
		{
			row = db.getRows().get(i);
			wv = new WineVector();
			wv.properties.put(Constants.Output.id, row.getValueByKey(Constants.WineDB.id).trim());
			wv.properties.put(Constants.Output.winename, row.getValueByKey(Constants.WineDB.winename).trim());
			wv.properties.put(Constants.Output.winery, row.getValueByKey(Constants.WineDB.winery).trim());
			wv.properties.put(Constants.Output.ava, row.getValueByKey(Constants.WineDB.ava).trim());
			wv.properties.put(Constants.Output.vintage, row.getValueByKey(Constants.WineDB.vintage).trim());
			wv.properties.put(Constants.Output.price, row.getValueByKey(Constants.WineDB.price).trim().replace("$", "").replace("NA", "0"));
			wv.properties.put(Constants.Output.rating, ""+calcualteRatingFromStars(row.getValueByKey(Constants.WineDB.rating)));
			wv.properties.put(Constants.Output.notes, row.getValueByKey(Constants.WineDB.notes).trim());
			wv.properties.put(Constants.Output.region, row.getValueByKey(Constants.WineDB.region).trim());
			wv.properties.put(Constants.Output.type, row.getValueByKey(Constants.WineDB.type).trim());
			wv.properties.put(Constants.Output.varietal, row.getValueByKey(Constants.WineDB.varietal).trim());
			
			vects.add(wv);
		}
		
		return vects;
	}
	
	private double calcualteRatingFromStars(String rating)
	{
		return rating.trim().replace(" ", "").replace("1/2", "#").replace("*", "##").length()/2.0;
	}
	
	private ArrayList<TagVector> getTagVectorsForWineVector(WineVector wv, HashMap<String, TagVector> wordToTVMap)
	{
		String notes = wv.properties.get(Constants.Output.notes);
		ArrayList<String> tokens = tokenizeLine(notes);
		
		ArrayList<TagVector> tvs = new ArrayList<TagVector>();
		String token = null;
		TagVector tv = null;
		for(int j = 0; j < tokens.size(); j++)
		{
			token = tokens.get(j);
			tv = wordToTVMap.get(token.toLowerCase());
			if(tv != null)
				tvs.add(tv);
		}
		
		return tvs;
	}

	
	/*************************************************************************************
	 * Wine Vector Calculation Methods
	 *************************************************************************************/
	
	private void processWineNotesIntoVectors(ArrayList<WineVector> vects, HashMap<String, TagVector> wordToTVMap)
	{
		WineVector wv = null;
		for(int i = 0; i < vects.size(); i++)
		{
			wv = vects.get(i);
			ArrayList<TagVector> tvs = getTagVectorsForWineVector(wv, wordToTVMap);
			calculateFloatsFromTVAggregate(wv, tvs);
		}
	}
	
	/*
	 * This is where things get a bit scary.
	 * 
	 * left = avg(tvs.def.j);
	 * right = Math.pow(lambda, tv.count) * sum(tvs.i)
	 * 
	 * forall(tvs.filter, filter.i( ((left) + (right)) / (def && nodef > 0 ? 2 : 1) ))
	 */
	private void calculateFloatsFromTVAggregate(WineVector wv, ArrayList<TagVector> tvs)
	{
		ArrayList<TagVector> def = new ArrayList<TagVector>();
		ArrayList<TagVector> nodef = new ArrayList<TagVector>();
		ArrayList<String> filters = new ArrayList<String>();
		
		TagVector tv = null;
		for(int i = 0; i < tvs.size(); i++)
		{
			tv = tvs.get(i);
			
			if(tv.isDefining){
				def.add(tv);
				if(tv.effect != null && !tv.effect.isEmpty())
					filters.add(tv.effect);
			}
			else
				nodef.add(tv);
		}

		HashMap<String, Double> defAvgVect = constructAvgVector(def);
		HashMap<String, Double> noDefSumVect = constructDecayedSumVector(nodef);
		HashMap<String, Double> mergedVect = mergeVectors(defAvgVect, noDefSumVect);
		
		filterVector(mergedVect, filters);
		
		for(String aroma : Constants.TagVector.aromas)
			wv.properties.put(Constants.TagVector.aromaIOMap.get(aroma), mergedVect.get(aroma).toString());
	}
	
	private HashMap<String, Double> mergeVectors(HashMap<String, Double> defAvgVect, HashMap<String, Double> noDefSumVect)
	{
		HashMap<String, Double> mergedVect = new HashMap<String, Double>();
		
		for(String aroma : Constants.TagVector.aromas)
		{
			Double val = 0.0;
			Double ndval = noDefSumVect.get(aroma);
			Double dval = defAvgVect.get(aroma);
			double div = ndval != null && !ndval.equals(Double.NaN) && 
						 dval != null && !dval.equals(Double.NaN) 
						 ? 2.0 : 1.0;
			
			if(ndval == null || ndval.equals(Double.NaN)) ndval = 0.0;
			if(dval == null || dval.equals(Double.NaN)) dval = 0.0;
			
			val = (dval + ndval) / div;
			
			mergedVect.put(aroma, val);
		}
		
		return mergedVect;
	}
	
	private void filterVector(HashMap<String, Double> v, ArrayList<String> filters)
	{
		String f = null;
		for(int i = 0; i < filters.size(); i++)
		{
			f = filters.get(i);
			if(f.equals("lower"))		lowerWineVector(v);
			else if(f.equals("raise"))	raiseWineVector(v);
			else if(f.equals("balance"))balanceWineVector(v);
		}
	}
	
	//20% reduction to difference from average
	private void balanceWineVector(HashMap<String, Double> wv)
	{
		//This average is the average across all of the attributes of the single merged vector
		Double avg = 0.0;
		for(String aroma : Constants.TagVector.aromas)
			avg += wv.get(aroma);
		avg /= Constants.TagVector.aromas.size();
		
		Double val = 0.0;
		for(String aroma : Constants.TagVector.aromas)
		{
			val = wv.get(aroma);
			if(!val.isNaN() && val > 0.0)
				wv.put(aroma, val + 0.2 * (avg - val));
		}
	}
	
	//20% of average boost to all values non-sero
	private void raiseWineVector(HashMap<String, Double> wv)
	{
		//This average is the average across all of the attributes of the single merged vector
		Double avg = 0.0;
		for(String aroma : Constants.TagVector.aromas)
			avg += wv.get(aroma);
		avg /= Constants.TagVector.aromas.size();
		
		Double val = 0.0;
		for(String aroma : Constants.TagVector.aromas)
		{
			val = wv.get(aroma);
			if(!val.isNaN() && val > 0.0)
				wv.put(aroma, val + 0.2 * (avg));
		}
	}
	
	//20% of average reduction for values > that value
	//else a 50% reduction is applied directly
	private void lowerWineVector(HashMap<String, Double> wv)
	{
		//This average is the average across all of the attributes of the single merged vector
		Double avg = 0.0;
		for(String aroma : Constants.TagVector.aromas)
			avg += wv.get(aroma);
		avg /= Constants.TagVector.aromas.size();
		
		Double val = 0.0;
		for(String aroma : Constants.TagVector.aromas)
		{
			val = wv.get(aroma);
			if(val > 0.2 * (avg))
				wv.put(aroma, val - 0.2 * (avg));
			else
				wv.put(aroma, 0.5 * val);
		}
	}
	
	private HashMap<String, Double> constructAvgVector(ArrayList<TagVector> tvs)
	{
		HashMap<String, Double> v = new HashMap<String, Double>();
		
		TagVector tv = null;
		for(String aroma : Constants.TagVector.aromas)
		{
			Double sum = 0.0;
			int count = 0;
			for(int i = 0; i < tvs.size(); i++)
			{
				tv = tvs.get(i);
				if(tv.descriptors.get(aroma).equals(Double.NaN))
					continue;
				sum += tv.descriptors.get(aroma);
				count++;
			}
			
			v.put(aroma, sum/count);
		}
		
		return v;
	}
	
	private HashMap<String, Double> constructDecayedSumVector(ArrayList<TagVector> tvs)
	{
		HashMap<String, Double> v = new HashMap<String, Double>();
		
		TagVector tv = null;
		for(String aroma : Constants.TagVector.aromas)
		{
			Double sum = 0.0;
			int count = 0;
			for(int i = 0; i < tvs.size(); i++)
			{
				tv = tvs.get(i);
				if(tv.descriptors.get(aroma).equals(Double.NaN))
					continue;
				sum += tv.descriptors.get(aroma);
				count++;
			}
			
			v.put(aroma, count > 0 ? Math.pow(DECAY_LAMBDA, count) * sum : Double.NaN);
		}
		
		return v;
	}

	private void normalizeWineVectors(ArrayList<WineVector> wvs)
	{
		HashMap<String, Double> maxValues = calculateMaxVector(wvs);
		
		WineVector wv = null;
		for(int i = 0; i < wvs.size(); i++)
		{
			wv = wvs.get(i);
			
			Double currVal = null;
			Double maxVal = null;
			String key = null;
			Double magnitude = 0.0;
			
			//SCALE IN REFERENCE TO MAXIMUM
			for(String aroma : Constants.TagVector.aromas)
			{
				key = Constants.TagVector.aromaIOMap.get(aroma);
				currVal = new Double(wv.properties.get(key));
				maxVal = maxValues.get(key);
				if(maxVal.isNaN())
					maxVal = 1.0;
				
				currVal = currVal / maxVal;
				//magnitude += Math.pow(currVal, 2.0);
				
				wv.properties.put(key, (new Double(currVal)).toString());
			}
			
			//magnitude = Math.sqrt(magnitude);
			
			//NORMALIZE - DONT!!!!!!
			/*
			for(String aroma : Constants.TagVector.aromas)
			{
				key = Constants.TagVector.aromaIOMap.get(aroma);
				currVal = new Double(wv.properties.get(key));
				wv.properties.put(key, (new Double(currVal / magnitude)).toString());
			}
			*/
			
			//BOOST FLAVOR COMPONENTS!
			for(String aroma : Constants.TagVector.aromas)
			{
				if(!(aroma.equals(Constants.TagVector.bitter)
						|| aroma.equals(Constants.TagVector.sweet)
						|| aroma.equals(Constants.TagVector.sour)
						|| aroma.equals(Constants.TagVector.salty)))
				continue;
				key = Constants.TagVector.aromaIOMap.get(aroma);
				currVal = new Double(wv.properties.get(key));
				wv.properties.put(key, (new Double(currVal * 1.2)).toString());
			}
		}
	}
	
	private HashMap<String, Double> calculateMaxVector(ArrayList<WineVector> wvs)
	{
		HashMap<String, Double> maxValues = new HashMap<String, Double>();
		
		WineVector wv = null;
		for(int i = 0; i < wvs.size(); i++)
		{
			wv = wvs.get(i);

			Double currVal = null;
			Double maxVal = null;
			String key = null;
			for(String aroma : Constants.TagVector.aromas)
			{
				key = Constants.TagVector.aromaIOMap.get(aroma);
				currVal = new Double(wv.properties.get(key));
				maxVal = maxValues.get(key);
				if(maxVal == null || currVal > maxVal)
					maxVal = currVal;
					
				maxValues.put(key, maxVal);
			}
		}
		return maxValues;
	}
	

	/*************************************************************************************
	 * Output Methods
	 *************************************************************************************/
	
	private void outputTabSeparatedFile(ArrayList<WineVector> wvs)
	{
		SimplePrinter sp = new SimplePrinter("WineVectors_TabSeparated.dat");
		boolean first = true;
		
		for(String key : Constants.Output.set)
		{
			if(!first)
				sp.print("\t");
			first = first ? !first : first;
			sp.print(key);	
		}
		sp.print("\n");
		
		WineVector wv = null;
		for(int i = 0; i < wvs.size(); i++)
		{
			wv = wvs.get(i);
			first = true;
			String val = null;
			for(String key : Constants.Output.set)
			{
				if(!first)
					sp.print("\t");
				first = first ? !first : first;
				val = wv.properties.get(key);
				if(val == null)
					val = "";
				sp.print(val.replace("\t", "   "));
			}
			sp.print("\n");
		}
		
		sp.close();
	}
	
	private void outputCSV(ArrayList<WineVector> wvs)
	{
		CSV out = new CSV();
		
		ArrayList<String> labels = new ArrayList<String>();
		for(String key : Constants.Output.set)
			labels.add(key);
		CSVHeaderRow header = new CSVHeaderRow(labels);
		out.setHeaderRow(header);
		
		ArrayList<CSVRow> rows = new ArrayList<CSVRow>();
		CSVRow row = null;
		WineVector wv = null;
		for(int i = 0; i < wvs.size(); i++)
		{
			row = new CSVRow(header);
			wv = wvs.get(i);
			String val = null;
			for(String key : Constants.Output.set){

				val = wv.properties.get(key);
				if(val == null)
					val = "";
				row.putMappedPair(key, val);
			}
			rows.add(row);
		}
		out.setRows(rows);
		
		out.saveAs("WineVectors_CSV.csv");
	}
	
	private void outputDatabaseScript(ArrayList<WineVector> wvs)
	{
		//INSERT INTO Books
		//VALUES (103, 'Test Title', 'Airite Books', 1980);
		SimplePrinter sp = new SimplePrinter("WineVectors_SQLInjection.sql");
		boolean first = true;
		WineVector wv = null;
		for(int i = 0; i < wvs.size(); i++)
		{
			sp.print("INSERT INTO Wines VALUES(");
			wv = wvs.get(i);
			first = true;
			for(String key : Constants.Output.set)
			{
				if(key.equals(Constants.Output.price) || key.equals(Constants.Output.region))
					continue;
				
				if(!first)
					sp.print(", ");
				first = first ? !first : first;
				
				if(key.equals(Constants.Output.ava)) {
					sp.print("\"" + wv.properties.get(Constants.Output.ava).replace("\t", " ")
							+ " - " + wv.properties.get(Constants.Output.region).replace("\t", " ") + "\"");
					continue;
				}
				
				//Print ints
				if(key.equals(Constants.Output.vintage) || key.equals(Constants.Output.id) 
						|| key.equals(Constants.Output.custerid) || key.equals(Constants.Output.cso)){
					if(wv.properties.get(key) == null)
						sp.print("0");
					else
						sp.print(wv.properties.get(key).replace("\t", " "));
				}
				//print floats
				else if(Constants.Output.aromas.contains(key) /*|| key.equals(Constants.Output.price)*/ 
						|| key.equals(Constants.Output.rating)){
					if(wv.properties.get(key) == null)
						sp.print("0.0");
					else
						sp.print(wv.properties.get(key).replace("\t", " "));
				}
				else{
					if(wv.properties.get(key) == null)
						sp.print("\"\"");
					else
						sp.print("\"" +wv.properties.get(key).replace("\t", " ")  + "\"");
				}
			}
			sp.print(");\n");
		}
		
		sp.close();
	}
	

	/*************************************************************************************
	 * Debug Methods
	 *************************************************************************************/
	
	private void debugDumpWineVector(ArrayList<WineVector> wvs)
	{
		WineVector wv = null;
		System.out.println("Total Wines: " + wvs.size());
		for(int i = 0; i < wvs.size(); i++)
		{
			wv = wvs.get(i);
			for(String key : Constants.Output.set)
			{
				System.out.print(" | " + col(wv.properties.get(key), 10));
			}
			System.out.println();
		}
	}

	/*************************************************************************************
	 * Helper Methods
	 *************************************************************************************/
	
	private ArrayList<String> tokenizeLine(String line)
	{
		ArrayList<String> tokens = new ArrayList<String>();
		String buf = "";
		char c = 0;
		int len = line.length();
		
		//Convert the line into a series of tokens delimited by white space
		for(int i = 0; i < len; i++)
		{
			c = line.charAt(i);
			if(isDelimiter(c)) {
				if(!buf.isEmpty()){
					tokens.add(buf);
					buf = "";
				}
			}else
				buf += c;
		}
		if(!buf.isEmpty())
			tokens.add(buf);
		return tokens;
	}
	
	private boolean isDelimiter(char c)
	{
		return Character.isWhitespace(c)
				|| c == ','	|| c == '<'
				|| c == '>'	|| c == '.'
				|| c == '/'	|| c == '?'
				|| c == ';'	|| c == ':'
				|| c == '\''|| c == '\"'
				|| c == '[' || c == '{'
				|| c == ']' || c == '}'
				|| c == '\\'|| c == '|'
				|| c == '-'	|| c == '_'
				|| c == '+'	|| c == '='
				|| c == '`'	|| c == '~'
				|| c == '!' || c == '@'
				|| c == '#'	|| c == '$'
				|| c == '%'	|| c == '^'
				|| c == '&'	|| c == '*'
				|| c == '('	|| c == ')';
	}
	
	private String col(String str, int width)
	{
		String fixedStr;
		if(str == null)
			str = "null";
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
	
	/*************************************************************************************
	 * Private Classes
	 *************************************************************************************/
	
	private class TagVector
	{
		public String word;
		public String key;
		public boolean isDefining;
		public String effect;
		public HashMap<String, Double> descriptors;
		
		public TagVector(String word, String key)
		{
			this.word = word;
			this.key = key;
			isDefining = false;
			effect = "";
			descriptors = new HashMap<String, Double>();
		}
	}
	
	private class WineVector
	{
		public HashMap<String, String> properties;
		
		public WineVector()
		{
			properties = new HashMap<String, String>();
		}
		
		public CSVRow toRow(CSVHeaderRow header)
		{
			CSVRow row = new CSVRow(header);
			for(String key : Constants.Output.set)
				row.putMappedPair(key, properties.get(key));
			return row;
		}
	}
	
	@SuppressWarnings(value = { "unused" })
	private static class Constants
	{
		public static class TagVector
		{
			public static final HashSet<String> set = new HashSet<String>();
			public static final HashSet<String> aromas = new HashSet<String>();
			public static final HashMap<String, String> aromaIOMap = new HashMap<String, String>();
			public static final String word = PutnSet.add(set, "Word");
			public static final String key = PutnSet.add(set, "Key");
			public static final String count = PutnSet.add(set, "Count");
			public static final String keep = PutnSet.add(set, "Keep");
			public static final String filter = PutnSet.add(set, "Filter");
			public static final String define = PutnSet.add(set, "Defining");
			public static final String bitter = PutnSet.add(aromas, PutnSet.add(set, "Bitter"));
			public static final String sweet = PutnSet.add(aromas, PutnSet.add(set, "Sweet"));
			public static final String sour = PutnSet.add(aromas, PutnSet.add(set, "Sour"));
			public static final String salty = PutnSet.add(aromas, PutnSet.add(set, "Salty"));
			public static final String chemical = PutnSet.add(aromas, PutnSet.add(set, "Chemical"));
			public static final String pungent = PutnSet.add(aromas, PutnSet.add(set, "Pungent"));
			public static final String oxidized = PutnSet.add(aromas, PutnSet.add(set, "Oxidized"));
			public static final String microbio = PutnSet.add(aromas, PutnSet.add(set, "Microbiological"));
			public static final String floral = PutnSet.add(aromas, PutnSet.add(set, "Floral"));
			public static final String spicy = PutnSet.add(aromas, PutnSet.add(set, "Spicy"));
			public static final String fruity = PutnSet.add(aromas, PutnSet.add(set, "Fruity"));
			public static final String vege = PutnSet.add(aromas, PutnSet.add(set, "Vegetative"));
			public static final String nutty = PutnSet.add(aromas, PutnSet.add(set, "Nutty"));
			public static final String caramel = PutnSet.add(aromas, PutnSet.add(set, "Caramelized"));
			public static final String woody = PutnSet.add(aromas, PutnSet.add(set, "Woody"));
			public static final String earthy = PutnSet.add(aromas, PutnSet.add(set, "Earthy"));
			public static final String effect = PutnSet.add(set, "Effect");
			
			static{
				for(String aroma : aromas)
					aromaIOMap.put(aroma, aroma.toLowerCase());
			}
		}
		
		public static class WineDB
		{
			public static final HashSet<String> set = new HashSet<String>();
			public static final String id = PutnSet.add(set, "ID");
			public static final String winery = PutnSet.add(set, "Winery");
			public static final String winename = PutnSet.add(set, "Wine Name");
			public static final String ava = PutnSet.add(set, "AVA");
			public static final String vintage = PutnSet.add(set, "Vintage");
			public static final String price = PutnSet.add(set, "$");
			public static final String rating = PutnSet.add(set, "Rating");
			public static final String notes = PutnSet.add(set, "Notes");
			public static final String region = PutnSet.add(set, "Region");
			public static final String type = PutnSet.add(set, "Type");
			public static final String varietal = PutnSet.add(set, "Main Varietal");
			public static final String tastingDate = PutnSet.add(set, "Tasting Date");
			public static final String pubDate = PutnSet.add(set, "Publication Date");
			public static final String setting = PutnSet.add(set, "Setting");
			public static final String acquisition = PutnSet.add(set, "Purchased/ Provided");
			public static final String temp = PutnSet.add(set, "Temp (if not standard)");
			public static final String link = PutnSet.add(set, "Hyperlink");
		}
		
		public static class Output
		{
			public static final LinkedHashSet<String> set = new LinkedHashSet<String>();
			public static final LinkedHashSet<String> aromas = new LinkedHashSet<String>();
			public static final String id = PutnSet.add(set, "wineID");
			public static final String winename = PutnSet.add(set, "wineName");
			public static final String varietal = PutnSet.add(set, "varietal");
			public static final String winery = PutnSet.add(set, "winery");
			public static final String type = PutnSet.add(set, "type");
			public static final String vintage = PutnSet.add(set, "vintage");
			public static final String ava = PutnSet.add(set, "ava");
			public static final String region = PutnSet.add(set, "region");
			public static final String custerid = PutnSet.add(set, "clusterID");
			public static final String cso = PutnSet.add(set, "CSO");
			public static final String tags = PutnSet.add(set, "tags");
			public static final String notes = PutnSet.add(set, "notes");
			public static final String rating = PutnSet.add(set, "rating");
			public static final String price = PutnSet.add(set, "price");
			public static final String imagepath = PutnSet.add(set, "imagePath");
			public static final String barcode = PutnSet.add(set, "barcode");
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
		
		public static class Intermediate
		{
			public static final String tagVectors = "tagvectors";
		}
	}

	/*************************************************************************************
	 * Main
	 *************************************************************************************/
	
	public static void main(String[] args)
	{
		WineReviewVectorGenerator gen = new WineReviewVectorGenerator();
		gen.run();
	}
}
