package util;

import java.util.HashSet;
import java.util.List;

public class PutnSet {
	
	public static <T> T add(HashSet<T> set, T t)
	{
		set.add(t);
		return t;
	}
	
	public static <T> T add(List<T> list, T t)
	{
		list.add(t);
		return t;
	}

}
