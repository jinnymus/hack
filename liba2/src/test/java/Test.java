import org.liba2.Duplicator;

import java.util.stream.IntStream;

public class Test {

    @org.junit.Test
    public void test() {
        Duplicator duplicator = new Duplicator();

        IntStream.range(1, 5000)
                .parallel()
                .forEach(i -> duplicator.isDuplicated("sad"));
    }
}
