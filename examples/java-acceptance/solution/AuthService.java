public final class AuthService {
    private AuthService() {}

    public static boolean authenticateToken(String token) {
        return token != null && token.startsWith("usr-") && token.length() > 4;
    }
}
