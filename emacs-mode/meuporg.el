
;;; meuporg.el --- Provides shortcuts for easier use of meup!org.

;; Copyright (C) 2012 Leo Perrin
;;
;; Author: Leo "picarresursix" Perrin <leoperrin@picarresursix.fr>
;; Created: 2012-12-20
;; Version: 0.9
;; Keywords: project management, data centralisation
;; URL: https://github.com/picarresursix/meuporg
;; Compatibility:  GNU Emacs 24.x
;;
;; This file is NOT part of GNU Emacs.
;;
;; This program is free software; you can redistribute it and/or
;; modify it under the terms of the GNU General Public License
;; as published by the Free Software Foundation; either version 2
;; of the License, or (at your option) any later version.
;;
;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.
;;
;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <http://www.gnu.org/licenses/>.
;;

;;; Commentary:
;;
;; Move this file somewhere in your emacs load-path. Then, add the following
;; to your .emacs file:
;; 
;; (load-file meuporg.el)
;; 
;;; Issues:
;;
;;; TODO:
;; 
;;; Change Log:
;;
;;; Code:

(setq meuporg-command "python2.7 ~/.meuporg ")

(defun meuporg-reload()
  "Reload the current meuporg main file after saving all buffers."
  (interactive)
  (save-some-buffers t)
  (shell-command (concat meuporg-command " -u"))
  (if (get-buffer "meup.*org.*")
      (revert-buffer "meup.*org.*")))

(defun meuporg-find-main()
  "Returns the path to meuporg of which the current file depends or an
empty string if there is no such meuporg."
  (setq old-buffer (current-buffer))
  (shell-command (concat meuporg-command " -f"))
  (switch-to-buffer "*Shell Command Output*")
  (setq path-to-main-meuporg
        (buffer-substring-no-properties (point-min) (- (point-max) 1)))
  (switch-to-buffer old-buffer)
  path-to-main-meuporg)

(defun meuporg-open-main()
  "Open the meuporg of which the current file depends (if any)."
  (interactive)
  (setq path-to-main-meuporg (meuporg-find-main))
  (if (< 2 (length path-to-main-meuporg))
      (progn
        (find-file path-to-main-meuporg)
        (message (concat "Opening " path-to-main-meuporg)))
      (message "No meuporg found.")))

(defun meuporg-insert-idea()
  "Inserts an IDEA meuporg item."
  (interactive)
  (insert "!IDEA! "))

(defun meuporg-insert-todo()
  "Inserts a TODO meuporg item."
  (interactive)
  (insert "!TODO! "))

(defun meuporg-insert-continue()
  "Inserts a TOCHECK meuporg item."
  (interactive)
  (insert "!CONTINUE! "))

(defun meuporg-insert-tocheck()
  "Inserts a TOCHECK meuporg item."
  (interactive)
  (insert "!TOCHECK! "))

(defun meuporg-insert-polish()
  "Inserts a TOCHECK meuporg item."
  (interactive)
  (insert "!POLISH! "))

(defun meuporg-insert-fixref()
  "Inserts a FIXREF meuporg item."
  (interactive)
  (insert "!FIXREF! "))

(defun meuporg-go-to-next-item()
  (interactive)
  (condition-case ex
      (search-forward-regexp "\![a-zA-Z0-9_]*\!")
    ('error
     (message "No items after cursor."))))

(defun meuporg-go-to-previous-item()
  (interactive)
  (condition-case ex
      (search-backward-regexp "\![a-zA-Z0-9_]*\!")
    ('error
     (message "No items before cursor."))))

(defun meuporg-list-items-in-buffer()
  "Lists the items in the current buffer and displays only them."
  (interactive)
  (loccur-no-highlight "![A-Za-z0-9_]+!")
  )

(defun meuporg-list-specific-items-in-buffer()
  "Prompts for a string and lists all the items in the file whose name
contains the said string."
  (interactive)
  (setq pattern
        (read-from-minibuffer "Search for items whose names contain: "))
  (loccur-no-highlight (concat "![A-zA-Z0-9]*" pattern "[A-zA-Z0-9]*!"))
  )

(defun meuporg-list-structure-of-buffer()
  "Searches for items with \"SECTION\" in their name and displays
them."
  (interactive)
  (loccur-no-highlight "![A-Za-z0-9_]*SECTION!")
  )

(global-unset-key (kbd "C-!"))

(define-minor-mode meuporg-mode
    "Toggle meuporg mode.

  Interactively with no argument, this command toggles the mode.
  A positive prefix argument enables the mode, any other prefix
  argument disables it.  From Lisp, argument omitted or nil enables
  the mode, `toggle' toggles the state. "
   ;; The initial value.
   :init-value nil
   ;; The indicator for the mode line.
   :lighter " !M!"
   :keymap
   `(
     (,(kbd "C-! u")   . meuporg-reload)
     (,(kbd "C-! m")   . meuporg-open-main)
     (,(kbd "C-! n")   . meuporg-go-to-next-item)
     (,(kbd "C-! p")   . meuporg-go-to-previous-item)
     (,(kbd "C-! l")   . meuporg-list-items-in-buffer)
     (,(kbd "C-! s")   . meuporg-list-specific-items-in-buffer)
     (,(kbd "C-! t")   . meuporg-list-structure-of-buffer)
     (,(kbd "C-! q")   . meuporg-kill-item-list)
     (,(kbd "C-! i i") . meuporg-insert-idea)
     (,(kbd "C-! i t") . meuporg-insert-todo)
     (,(kbd "C-! i c") . meuporg-insert-continue)
     (,(kbd "C-! i h") . meuporg-insert-tocheck)
     (,(kbd "C-! i p") . meuporg-insert-polish)
     (,(kbd "C-! i f") . meuporg-insert-fixref)))

(add-hook 'meuporg-mode-hook
          (lambda ()
            (font-lock-add-keywords
             nil
             '(("!\\([a-zA-Z0-9_]*\\)!" 1 font-lock-warning-face t)))))

(add-hook 'find-file-hook
          (lambda()
            (if (< 1 (length (meuporg-find-main)))
                (meuporg-mode))))

;;; meuporg.el ends here
