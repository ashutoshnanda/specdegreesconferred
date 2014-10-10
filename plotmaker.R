extract <- function(filename) {
    connection <- file(filename, open="r")
    lines <- readLines(connection)
    close(connection)
    total.headcount.line = lines[length(lines) - 1]
    total.headcount <- as.numeric(strsplit(total.headcount.line, "\t")[[1]][7])
    total.degrees.line = lines[length(lines)]
    total.degrees <- as.numeric(strsplit(total.degrees.line, "\t")[[1]][7])
    return(c(total.headcount, total.degrees))
}

import <- function() {
    range <- 2003:2010
    jpeg("Degrees and Headcounts by Year.jpg")
    a <- sapply(range, function(x) sprintf("data/cc-%d.tsv", x))
    b <- sapply(a, function(x) extract(x))
    plot(range, b[1, ], ylim = c(950, 1450), type = "b", col = 'red',
         xlab = "", ylab = "", pch = c(15))
    par(new = T)
    plot(range, b[2, ], ylim = c(950, 1450), type = "b", col = 'blue',
         xlab = "", ylab = "", pch = c(15))
    par(new = T)
    plot(range, b[2, ] / b[1, ], ylim = c(950, 1450), type = "b", col = 'blue',
         xlab = "", ylab = "")
    title("Degrees and Headcount by Year (Columbia College)", xlab = "Year", ylab = "Count")
    legend("topright", c("Headcount", "Degrees"), col = c("red", "blue"), 
           lty = c(1, 1), pch = c(15, 15))
    dev.off()
    jpeg("Achievement Factor.jpg")
    plot(range, b[1, ] / b[2, ], ylim = c(1, 1.5), type = "b", col = 'green',
         xlab = "Year", ylab = "Ratio", pch = c(15), 
         main = "Achievement Factor (Columbia College)")
    dev.off()
    return(b)
}