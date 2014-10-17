extract <- function(filename) {
    connection <- file(filename, open="r")
    lines <- readLines(connection)
    close(connection)
    total.headcount.line = lines[length(lines) - 1]
    print(total.headcount.line)
    total.headcount <- as.numeric(strsplit(total.headcount.line, "\t")[[1]][7])
    total.degrees.line = lines[length(lines)]
    total.degrees <- as.numeric(strsplit(total.degrees.line, "\t")[[1]][7])
    return(c(total.headcount, total.degrees))
}

import <- function(school) {
    long.school <- if(school == "cc") {
        "Columbia College"
    } else if(school == "en") {
        "Columbia Engineering"
    } else {
        "General Studies"
    }
    range <- 2003:2012
    jpeg(sprintf("Degrees and Headcounts by Year - %s.jpg", long.school))
    par(mar = c(8,4,4,2) + 0.1)
    a <- sapply(range, function(x) sprintf("data/%s-%d.tsv", school, x))
    b <- sapply(a, function(x) extract(x))
    print(b[1, ])
    limits <- c(0.75 * min(b[1, ]), 1.25 * max(b[1,]))
    plot(range, b[1, ], ylim = limits, type = "b", col = 'red',
         xlab = "", ylab = "", pch = c(15), xaxt = "n")
    par(new = T)
    plot(range, b[2, ], ylim = limits, type = "b", col = 'blue',
         xlab = "", ylab = "", pch = c(15), xaxt = "n")
    title(sprintf("Degrees and Headcount by Year (%s)", long.school), ylab = "Count")
    mtext("Graduating Class", side = 1, line = 6);
    legend("topleft", c("Headcount", "Degrees"), col = c("red", "blue"), 
           lty = c(1, 1), pch = c(15, 15))
    classes <- sapply(range, function(x) sprintf("%d-%d", x, x + 1))
    axis(1, at = range, labels = classes, las = 2)
    dev.off()
    jpeg(sprintf("Achievement Factor - %s.jpg", long.school))
    plot(range, b[1, ] / b[2, ], ylim = c(1, 1.5), type = "b", col = 'green',
         xlab = "Year", ylab = "Ratio", pch = c(15), 
         main = sprintf("Achievement Factor (%s)", long.school))
    dev.off()
}

all <- function() {
    import("cc")
    import("en")
    import("gs")
}