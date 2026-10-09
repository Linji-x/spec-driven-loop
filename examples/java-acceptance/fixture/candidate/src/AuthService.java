public final class AuthService {
    private AuthService() {}

    public static boolean authenticateToken(String token) {
        // Baseline defect: the prefix alone is incorrectly accepted.
        return token != null && token.startsWith("usr-");
    }
}
