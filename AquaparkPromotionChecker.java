import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class AquaparkPromotionChecker {

    private static final String PROMOTION_URL = "https://aquapark.wroc.pl/pl/cennik-karnetow-do-aquaparku";
    private static final String PROMOTION_KEYWORD = "4 miesiące w cenie 3";

    public static void main(String[] args) {
        try {
            if (isPromotionAvailable()) {
                System.out.println("Promocja '4 miesiące w cenie 3' jest dostępna.");
            } else {
                System.out.println("Promocja '4 miesiące w cenie 3' nie jest dostępna.");
            }
        } catch (IOException e) {
            System.err.println("Wystąpił błąd podczas sprawdzania promocji: " + e.getMessage());
        }
    }

    public static boolean isPromotionAvailable() throws IOException {
        URL url = new URL(PROMOTION_URL);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");

        try (Scanner scanner = new Scanner(connection.getInputStream())) {
            StringBuilder pageContent = new StringBuilder();
            while (scanner.hasNextLine()) {
                pageContent.append(scanner.nextLine());
            }
            return pageContent.toString().contains(PROMOTION_KEYWORD);
        }
    }
}
