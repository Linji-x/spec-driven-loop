public final class TokenClient {
    private TokenClient() {}

    public static boolean canSignIn(String token) {
        return AuthService.authenticateToken(token);
    }
}
