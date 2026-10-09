public final class AuthServiceAcceptance {
    private AuthServiceAcceptance() {}

    private static void check(String id, String token, boolean expected) {
        boolean actual = TokenClient.canSignIn(token);
        if (actual != expected) {
            throw new AssertionError(id + ": expected " + expected + ", got " + actual);
        }
        System.out.println("CASE " + id + " PASS");
    }

    public static void main(String[] args) {
        if (args.length != 1 || !args[0].matches("[a-f0-9]{64}")) {
            throw new IllegalArgumentException("Expected a fresh verifier completion challenge.");
        }
        check("valid_minimum", "usr-a", true);
        check("valid_long", "usr-user42", true);
        check("valid_unicode", "usr-用户", true);
        check("valid_whitespace_suffix", "usr- ", true);
        check("null_token", null, false);
        check("empty_token", "", false);
        check("wrong_prefix", "adm-a", false);
        check("missing_suffix", "usr-", false);
        check("leading_space", " usr-a", false);
        System.out.println("COMPLETE " + args[0]);
    }
}
